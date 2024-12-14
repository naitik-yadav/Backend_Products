# Generated by Django 4.2.4 on 2024-12-09 17:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Updated At')),
                ('request_json', models.JSONField(blank=True, null=True)),
                ('response_json', models.JSONField(blank=True, null=True)),
                ('request_status', models.CharField(blank=True, max_length=3)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Updated At')),
                ('request_json', models.JSONField(blank=True, null=True)),
                ('response_json', models.JSONField(blank=True, null=True)),
                ('request_status', models.CharField(blank=True, max_length=3)),
                ('order_status', models.CharField(choices=[('pending', 'Pending'), ('shipped', 'Shipped'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='Products.cart')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Updated At')),
                ('request_json', models.JSONField(blank=True, null=True)),
                ('response_json', models.JSONField(blank=True, null=True)),
                ('request_status', models.CharField(blank=True, max_length=3)),
                ('product_name', models.CharField(max_length=80)),
                ('product_number', models.IntegerField()),
                ('product_type', models.CharField(max_length=225)),
                ('description', models.CharField(max_length=225)),
                ('category', models.CharField(max_length=225)),
                ('Price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('images', models.ImageField(blank=True, null=True, upload_to='products/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Updated At')),
                ('request_json', models.JSONField(blank=True, null=True)),
                ('response_json', models.JSONField(blank=True, null=True)),
                ('request_status', models.CharField(blank=True, max_length=3)),
                ('quantity', models.IntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='Products.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Products.products')),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Updated At')),
                ('request_json', models.JSONField(blank=True, null=True)),
                ('response_json', models.JSONField(blank=True, null=True)),
                ('request_status', models.CharField(blank=True, max_length=3)),
                ('quantity', models.IntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='Products.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Products.products')),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
            },
        ),
    ]
