from django.apps import AppConfig


class BasePageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog_page'
