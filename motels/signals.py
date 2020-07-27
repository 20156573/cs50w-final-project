from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, RegularUserHistory, PostStatus

# tạo lịch sử
@receiver(post_save, sender=Post)
def create_history(sender, instance, created, **kwargs):
    if created:
        post_status = PostStatus.objects.get(pk=1)
        RegularUserHistory.objects.create(post_status=post_status, post=instance, updated_by=instance.poster)
# post_save.connect(create_history, sender=Post, dispatch_uid="unique_identifier")


