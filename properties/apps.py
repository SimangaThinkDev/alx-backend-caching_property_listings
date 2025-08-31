from django.apps import AppConfig


class PropertiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'properties'

    def ready(self):
        """
        This method is called when the Django application is ready.
        It's the perfect place to import signal handlers.
        """
        import properties.signals # We could also simply import .signals but to be specific
        