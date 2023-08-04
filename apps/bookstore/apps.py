from django.apps import AppConfig


class BookstoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.bookstore'

    def ready(self):
        import apps.bookstore.signals
