from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, RegularUserHistory

# tạo lịch sử
@receiver(post_save, sender=Post)
def create_history(sender, instance, created, **kwargs):
    if created:
        RegularUserHistory.objects.create(status=1, post=instance, updated_by=instance.poster)
    


