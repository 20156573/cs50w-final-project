# Generated by Django 3.0.7 on 2020-08-28 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0011_auto_20200828_1118'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vip',
            options={'verbose_name': 'Vip', 'verbose_name_plural': 'Vip'},
        ),
        migrations.RemoveField(
            model_name='postedads',
            name='vip',
        ),
        migrations.AddField(
            model_name='discount',
            name='vip',
            field=models.ManyToManyField(blank=True, related_name='passengers', to='finance.Vip'),
        ),
    ]
