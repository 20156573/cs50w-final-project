# Generated by Django 3.0.7 on 2020-07-25 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('motels', '0012_auto_20200725_1759'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AllFeedback',
            new_name='UserFeedback',
        ),
    ]