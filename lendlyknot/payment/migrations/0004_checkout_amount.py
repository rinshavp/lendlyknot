# Generated by Django 4.1.5 on 2024-02-28 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_remove_checkout_apartment_remove_checkout_country_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
