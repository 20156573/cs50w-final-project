# Generated by Django 3.0.7 on 2020-08-14 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('motels', '0004_auto_20200810_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.IntegerField(default=1),
        ),
    ]
