# Generated by Django 3.0.7 on 2020-09-02 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0016_auto_20200902_2234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='amount',
            field=models.ManyToManyField(blank=True, through='finance.VipDiscount', to='finance.Vip'),
        ),
    ]