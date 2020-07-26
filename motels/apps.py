from django.apps import AppConfig
from django.db.models.signals import post_save
from .models import Post
from .signals import *
class MotelsConfig(AppConfig):
    name = 'motels'

    # def ready(self):
    #     post_save.connect(create_history, sender = Post)