from django.apps import AppConfig


class AppWarblerConfig(AppConfig):
    name = 'app_warbler'

    def ready(self):
        import app_warbler.signals
