from django.test import TestCase

# Create your tests here.
import pytest
from django.test import TestCase
from django.db import models, connection
from django.core.exceptions import ImproperlyConfigured
from .models import NaturalKeyMixin , NaturalKeyManager


class BookWithExplicitNK(NaturalKeyMixin, models.Model):
    """Model with explicitly defined natural key fields."""
    NATURAL_KEY_FIELDS = ('isbn',)

    isbn = models.CharField(max_length=13, unique=True)
    title = models.CharField(max_length=255)

    class Meta:
        app_label = 'testapp'


class BookWithAutoNK(NaturalKeyMixin, models.Model):
    """Model that auto-detects natural key from unique field."""
    isbn = models.CharField(max_length=13, unique=True)
    title = models.CharField(max_length=255)

    class Meta:
        app_label = 'testapp'


class AuthorWithCompositeNK(NaturalKeyMixin, models.Model):
    """Model with composite natural key."""
    NATURAL_KEY_FIELDS = ('first_name', 'last_name')

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)

    class Meta:
        app_label = 'testapp'
        unique_together = [('first_name', 'last_name')]


class PublisherWithDependency(NaturalKeyMixin, models.Model):
    """Model with natural key dependencies."""
    NATURAL_KEY_FIELDS = ('name',)
    NATURAL_KEY_DEPENDENCIES = ('testapp.Country',)

    name = models.CharField(max_length=200, unique=True)
    country = models.ForeignKey('Country', on_delete=models.CASCADE)

    class Meta:
        app_label = 'testapp'


class Country(NaturalKeyMixin, models.Model):
    """Simple model for testing dependencies."""
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=100)

    class Meta:
        app_label = 'testapp'


# Invalid model for testing error cases
def create_invalid_model():
    """Create a model with no unique fields - should raise error."""
    class InvalidModel(NaturalKeyMixin, models.Model):
        title = models.CharField(max_length=255)

        class Meta:
            app_label = 'testapp'

    return InvalidModel


class TestNaturalKeyMixin(TestCase):
    """Test cases for NaturalKeyMixin functionality."""

    @classmethod
    def setUpTestData(cls):
        # Dynamically create the model tables in the test DB
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(Country)
            schema_editor.create_model(PublisherWithDependency)
            schema_editor.create_model(BookWithExplicitNK)
            schema_editor.create_model(BookWithAutoNK)
            schema_editor.create_model(AuthorWithCompositeNK)

    def test_explicit_natural_key_fields(self):
        """Test model with explicitly defined NATURAL_KEY_FIELDS."""
        book = BookWithExplicitNK(isbn='9780135957059', title='The Pragmatic Programmer')

        # Should use ISBN as natural key
        self.assertEqual(book.natural_key(), ('9780135957059',))

        # Manager should be NaturalKeyManager
        self.assertIsInstance(BookWithExplicitNK.objects, NaturalKeyManager)
        self.assertTrue(BookWithExplicitNK.objects.use_in_migrations)

    def test_auto_detected_natural_key(self):
        """Test model that auto-detects natural key from unique fields."""
        book = BookWithAutoNK(isbn='9780135957059', title='The Pragmatic Programmer')

        # Should auto-detect ISBN as natural key
        self.assertEqual(book.natural_key(), ('9780135957059',))

        # Should have correct internal fields
        self.assertEqual(BookWithAutoNK._get_natural_key_fields(), ('isbn',))

    def test_composite_natural_key(self):
        """Test model with composite natural key."""
        author = AuthorWithCompositeNK(
            first_name='Andrew',
            last_name='Hunt',
            bio='Co-author of The Pragmatic Programmer'
        )

        # Should return both fields in order
        self.assertEqual(author.natural_key(), ('Andrew', 'Hunt'))

    def test_get_by_natural_key(self):
        """Test manager's get_by_natural_key method."""
        # Create and save a book
        book = BookWithExplicitNK.objects.create(
            isbn='9780135957059',
            title='The Pragmatic Programmer'
        )

        # Should be able to retrieve by natural key
        retrieved = BookWithExplicitNK.objects.get_by_natural_key('9780135957059')
        self.assertEqual(retrieved.pk, book.pk)
        self.assertEqual(retrieved.title, book.title)

    def test_get_by_natural_key_composite(self):
        """Test get_by_natural_key with composite key."""
        author = AuthorWithCompositeNK.objects.create(
            first_name='Andrew',
            last_name='Hunt'
        )

        retrieved = AuthorWithCompositeNK.objects.get_by_natural_key('Andrew', 'Hunt')
        self.assertEqual(retrieved.pk, author.pk)

    def test_get_by_natural_key_wrong_args(self):
        """Test get_by_natural_key with wrong number of arguments."""
        with self.assertRaises(ValueError) as ctx:
            BookWithExplicitNK.objects.get_by_natural_key('isbn', 'extra')

        self.assertIn('Expected 1 natural key parts', str(ctx.exception))

    def test_natural_key_dependencies(self):
        """Test that dependencies are properly attached."""
        # Check that natural_key has dependencies attribute
        self.assertTrue(hasattr(PublisherWithDependency.natural_key, 'dependencies'))
        self.assertEqual(
            PublisherWithDependency.natural_key.dependencies,
            ('testapp.Country',)
        )

    def test_foreign_key_in_natural_key(self):
        """Test handling of foreign keys in natural keys."""
        country = Country.objects.create(code='US', name='United States')
        publisher = PublisherWithDependency(name='Addison-Wesley', country=country)

        # Natural key should include the country's natural key
        nk = publisher.natural_key()
        self.assertEqual(nk[0], 'Addison-Wesley')

    def test_no_unique_fields_raises_error(self):
        """Test that model without unique fields raises ImproperlyConfigured."""
        with self.assertRaises(ImproperlyConfigured) as ctx:
            create_invalid_model()

        self.assertIn('has no unique fields', str(ctx.exception))

    def test_unique_together_detection(self):
        """Test that unique_together is detected for natural keys."""
        # AuthorWithCompositeNK uses unique_together
        fields = AuthorWithCompositeNK._get_natural_key_fields()
        self.assertEqual(set(fields), {'first_name', 'last_name'})

    def test_manager_in_migrations(self):
        """Test that manager works in migrations."""
        self.assertTrue(BookWithExplicitNK.objects.use_in_migrations)
        self.assertTrue(BookWithAutoNK.objects.use_in_migrations)
        self.assertTrue(AuthorWithCompositeNK.objects.use_in_migrations)


# Additional test for unique field types
class TestUniqueFieldTypes(TestCase):
    """Test natural keys with different field types."""

    def test_slug_field(self):
        """Test with SlugField."""
        class Article(NaturalKeyMixin, models.Model):
            slug = models.SlugField(unique=True)
            title = models.CharField(max_length=200)

            class Meta:
                app_label = 'testapp'

        article = Article(slug='django-tips', title='Django Tips')
        self.assertEqual(article.natural_key(), ('django-tips',))

    def test_email_field(self):
        """Test with EmailField."""
        class User(NaturalKeyMixin, models.Model):
            email = models.EmailField(unique=True)
            name = models.CharField(max_length=100)

            class Meta:
                app_label = 'testapp'

        user = User(email='test@example.com', name='Test User')
        self.assertEqual(user.natural_key(), ('test@example.com',))

    def test_uuid_field(self):
        """Test with UUIDField."""
        import uuid

        class Token(NaturalKeyMixin, models.Model):
            key = models.UUIDField(unique=True, default=uuid.uuid4)
            name = models.CharField(max_length=100)

            class Meta:
                app_label = 'testapp'

        test_uuid = uuid.uuid4()
        token = Token(key=test_uuid, name='API Token')
        self.assertEqual(token.natural_key(), (test_uuid,))

    # @classmethod
    # def setUpTestData(cls):
    #     # Dynamically create the model tables in the test DB
    #     with connection.schema_editor() as schema_editor:
    #         schema_editor.create_model(Article)
    #         schema_editor.create_model(User)
    #         schema_editor.create_model(Token)

if __name__ == '__main__':
    # Run tests with pytest
    pytest.main([__file__])

