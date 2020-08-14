from django.apps import AppConfig


class MotelsConfig(AppConfig):
    name = 'motels'

    def ready(self):
        import motels.signals
