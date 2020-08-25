from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, RegularUserHistory, PostStatus

# tạo lịch sử
@receiver(post_save, sender=Post)
def create_history(sender, instance, created, **kwargs):
    if created:
        status = PostStatus.objects.get(pk=1)
        RegularUserHistory.objects.create(status=status, post=instance, updated_by=instance.poster)
    


