# Generated by Django 4.1.5 on 2024-03-21 21:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0025_booking_no_of_days_alter_booking_booking_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_image3',
        ),
    ]
