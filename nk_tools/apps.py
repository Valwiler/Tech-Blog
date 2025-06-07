from django.apps import AppConfig

"""
Django Natural Key Toolkit

A reusable mixin and manager pair that enables any Django model to use natural keys
for fixture serialization without brittle auto-incrementing primary keys.

Usage:
    from dktools.nk import NaturalKeyMixin, NaturalKeyManager

    class MyModel(NaturalKeyMixin, models.Model):
        NATURAL_KEY_FIELDS = ('slug',)
        slug = models.SlugField(unique=True)
        title = models.CharField(max_length=255)

        # Manager is automatically added by mixin, but can be explicit:
        objects = NaturalKeyManager()
"""

class NkToolsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nk_tools'

