# Generated by Django 3.0.7 on 2020-09-02 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0022_remove_discount_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='amount',
            field=models.ManyToManyField(blank=True, to='finance.Vip'),
        ),
    ]
