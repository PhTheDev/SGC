from django.apps import AppConfig

class AppSgcConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_sgc'

    def ready(self):
        import app_sgc.signals
