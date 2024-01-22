# Generated by Django 5.0.1 on 2024-01-18 17:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, default='', max_length=200)),
                ('product_list', models.CharField(default='error', max_length=1000)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('payment_date', models.DateTimeField(blank=True, default='None')),
                ('summary_price', models.PositiveIntegerField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['order_date'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=100)),
                ('description', models.CharField(blank=True, default='', max_length=500)),
                ('price', models.PositiveIntegerField()),
                ('image', models.ImageField(upload_to=None)),
                ('image_min', models.ImageField(max_length=50, upload_to=None)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restapi.category')),
            ],
        ),
    ]
