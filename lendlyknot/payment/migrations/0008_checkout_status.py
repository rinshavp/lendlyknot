# Generated by Django 4.1.5 on 2024-03-04 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0007_rename_payement_id_checkout_payment_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='status',
            field=models.CharField(default='Pending', max_length=254, verbose_name='Payment Status'),
        ),
    ]