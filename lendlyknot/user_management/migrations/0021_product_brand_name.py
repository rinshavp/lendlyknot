# Generated by Django 4.1.5 on 2024-02-24 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0020_product_product_image1_product_product_image2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]