# Generated by Django 4.1.5 on 2024-02-11 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0012_rename_desc_product_product_desc_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='productSize',
        ),
        migrations.AddField(
            model_name='product',
            name='size_l_qty',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='size_m_qty',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='size_s_qty',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='size_xl_qty',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='size_xxl_qty',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='size_xxxl_qty',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='ProductSize',
        ),
    ]