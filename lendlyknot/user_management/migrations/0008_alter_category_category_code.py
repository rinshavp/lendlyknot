# Generated by Django 4.1.5 on 2024-02-06 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0007_alter_category_category_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_code',
            field=models.CharField(default=1, max_length=255, unique=True),
        ),
    ]
