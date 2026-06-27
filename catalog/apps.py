from django.apps import AppConfig


class CatalogConfig(AppConfig):
    name = "catalog"


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from . import signals
