from django.apps import AppConfig


class CafeteriaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.cafeteria'

    def ready(self):
        import apps.cafeteria.signals
