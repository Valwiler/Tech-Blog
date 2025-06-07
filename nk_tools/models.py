from django.core.exceptions import ImproperlyConfigured
from django.db import models


class NaturalKeyManager(models.Manager):
    """Manager that supports natural key lookups and works in migrations."""

    use_in_migrations = True

    def get_by_natural_key(self, *args):
        """
        Retrieve an instance by its natural key parts.

        Args:
            *args: Values corresponding to NATURAL_KEY_FIELDS in order

        Returns:
            Model instance matching the natural key

        Raises:
            Model.DoesNotExist: If no matching instance found
            Model.MultipleObjectsReturned: If multiple instances match
        """
        if not hasattr(self.model, 'NATURAL_KEY_FIELDS'):
            raise ImproperlyConfigured(
                f"{self.model.__name__} must define NATURAL_KEY_FIELDS to use natural keys"
            )

        fields = self.model._get_natural_key_fields()

        if len(args) != len(fields):
            raise ValueError(
                f"Expected {len(fields)} natural key parts for {self.model.__name__}, "
                f"got {len(args)}"
            )

        lookup = dict(zip(fields, args))
        return self.get(**lookup)


class NaturalKeyMixinBase:
    """Base functionality for NaturalKeyMixin without metaclass interference."""

    @classmethod
    def _get_natural_key_fields(cls):
        """
        Get the fields that constitute the natural key.

        Returns explicit NATURAL_KEY_FIELDS if defined, otherwise auto-detects
        unique fields (excluding primary key).

        Returns:
            tuple: Field names that form the natural key

        Raises:
            ImproperlyConfigured: If no suitable fields found
        """
        # Use explicit fields if defined
        if hasattr(cls, 'NATURAL_KEY_FIELDS') and cls.NATURAL_KEY_FIELDS:
            return cls.NATURAL_KEY_FIELDS

        # Auto-detect unique fields
        unique_fields = []
        for field in cls._meta.get_fields():
            if (hasattr(field, 'unique') and field.unique and
                not field.primary_key and
                not isinstance(field, models.ManyToManyField)):
                unique_fields.append(field.name)

        # Check for unique_together
        if not unique_fields and cls._meta.unique_together:
            # Use first unique_together constraint
            unique_fields = list(cls._meta.unique_together[0])

        if not unique_fields:
            raise ImproperlyConfigured(
                f"{cls.__name__} has no unique fields and NATURAL_KEY_FIELDS is not defined. "
                f"Define NATURAL_KEY_FIELDS or add unique=True to at least one field."
            )

        return tuple(sorted(unique_fields))  # Sort for consistency

    def natural_key(self):
        """
        Return the natural key for this instance.

        Returns:
            tuple: Values of fields that uniquely identify this instance
        """
        fields = self._get_natural_key_fields()
        values = []

        for field_name in fields:
            value = getattr(self, field_name)

            # Handle foreign keys by getting their natural key
            field = self._meta.get_field(field_name)
            if isinstance(field, models.ForeignKey):
                if value and hasattr(value, 'natural_key'):
                    value = value.natural_key()
                elif value:
                    value = value.pk

            values.append(value)

        return tuple(values)


class NaturalKeyMetaclass(models.base.ModelBase):
    """Metaclass that adds natural key functionality to models."""

    def __new__(mcs, name, bases, attrs, **kwargs):
        # Create the class first
        cls = super().__new__(mcs, name, bases, attrs, **kwargs)

        # Skip setup for abstract models or the mixin itself
        if (getattr(cls._meta, 'abstract', True) or
            name in ('NaturalKeyMixin', 'NaturalKeyMixinBase')):
            return cls

        # Add the manager if not explicitly defined
        if not hasattr(cls, 'objects') or not isinstance(cls.objects, NaturalKeyManager):
            cls.add_to_class('objects', NaturalKeyManager())

        # Add dependencies to natural_key method if specified
        if hasattr(cls, 'NATURAL_KEY_DEPENDENCIES'):
            original_natural_key = cls.natural_key
            cls.natural_key = original_natural_key
            cls.natural_key.dependencies = cls.NATURAL_KEY_DEPENDENCIES

        # Validate configuration at import time
        try:
            cls._get_natural_key_fields()
        except ImproperlyConfigured as e:
            # Only raise if this is a concrete model
            if not cls._meta.abstract:
                raise

        return cls


class NaturalKeyMixin(NaturalKeyMixinBase, models.Model, metaclass=NaturalKeyMetaclass):
    """
    Mixin that provides natural key functionality to Django models.

    Usage:
        class MyModel(NaturalKeyMixin, models.Model):
            NATURAL_KEY_FIELDS = ('slug',)  # Optional - will auto-detect unique fields
            NATURAL_KEY_DEPENDENCIES = ('myapp.OtherModel',)  # Optional

            slug = models.SlugField(unique=True)
            title = models.CharField(max_length=255)

    The mixin automatically:
    - Adds a NaturalKeyManager as 'objects'
    - Provides natural_key() method
    - Auto-detects unique fields if NATURAL_KEY_FIELDS not specified
    - Handles dependencies via natural_key.dependencies
    """

    NATURAL_KEY_FIELDS = ()

    class Meta:
        abstract = True
