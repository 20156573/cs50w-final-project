# Generated by Django 3.0.7 on 2020-08-10 15:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('motels', '0002_auto_20200731_1508'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postfollow',
            name='follower',
        ),
        migrations.AddField(
            model_name='postfollow',
            name='follower',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='followers', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
