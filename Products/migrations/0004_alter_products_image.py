# Generated by Django 5.2 on 2025-05-09 10:49

import Products.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0003_remove_products_images_products_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='products/', validators=[Products.models.validate_file_extension]),
        ),
    ]
