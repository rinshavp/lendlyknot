# Generated by Django 4.1.5 on 2024-02-27 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0022_booking_amount_alter_booking_booking_status_payment_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='booking',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='user',
        ),
        migrations.DeleteModel(
            name='Checkout',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
    ]
