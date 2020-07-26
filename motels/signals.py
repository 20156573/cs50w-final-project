from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, RegularUserHistory, PostStatus

@receiver(post_save, sender=Post)
def create_history(sender, instance, created, **kwargs):
    if created:
        post_status = PostStatus.objects.get(pk=1)
        RegularUserHistory.objects.create(post_status=post_status, post=instance, updated_by=instance.poster)
        
@receiver(post_save, sender=Post)
def save_history(sender, instance, **kwargs):
    instance.post.save()

# post_save.connect(create_history, sender=Post, dispatch_uid="unique_identifier")


