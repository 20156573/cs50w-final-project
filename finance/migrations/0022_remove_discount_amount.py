# Generated by Django 3.0.7 on 2020-09-02 22:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0021_auto_20200902_2243'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discount',
            name='amount',
        ),
    ]
