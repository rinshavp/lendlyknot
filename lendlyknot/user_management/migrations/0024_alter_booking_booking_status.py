# Generated by Django 4.1.5 on 2024-03-04 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0023_remove_payment_booking_remove_payment_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_status',
            field=models.CharField(choices=[('1', 'Booked'), ('2', 'Returned'), ('3', 'Cancelled'), ('4', 'Delivered'), ('5', 'Initialised')], default=5, max_length=2),
        ),
    ]