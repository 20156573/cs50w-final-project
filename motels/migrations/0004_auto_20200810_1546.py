# Generated by Django 3.0.7 on 2020-08-10 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('motels', '0003_auto_20200810_1542'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='postfollow',
            unique_together={('post', 'follower')},
        ),
    ]