# Generated by Django 3.0.7 on 2020-08-23 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardhistory',
            name='status',
            field=models.IntegerField(default=99),
        ),
    ]
