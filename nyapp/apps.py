from django.apps import AppConfig

class NyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nyapp'

    def ready(self):
        pass
