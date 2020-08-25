from django.apps import AppConfig


class MotelsConfig(AppConfig):
    name = 'motels'
    verbose_name = "Chung"
        
    def ready(self):
        import motels.signals
