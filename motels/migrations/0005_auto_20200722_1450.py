# Generated by Django 3.0.7 on 2020-07-22 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('motels', '0004_auto_20200713_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='furniture',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='renters_gender',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=110),
        ),
    ]
