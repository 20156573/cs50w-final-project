# Generated by Django 3.0.7 on 2020-08-27 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('motels', '0012_auto_20200827_0855'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otherfeedback',
            name='post',
        ),
        migrations.DeleteModel(
            name='PostStatus',
        ),
        migrations.DeleteModel(
            name='OtherFeedback',
        ),
    ]
