# Generated by Django 5.0.1 on 2024-01-23 22:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0013_alter_order_order_date_alter_order_payment_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from', models.DateTimeField(default=datetime.datetime(1924, 1, 22, 11, 42, 5, 2006, tzinfo=datetime.timezone.utc))),
                ('date_to', models.DateTimeField(default=datetime.datetime(2124, 1, 22, 11, 42, 5, 2006, tzinfo=datetime.timezone.utc))),
                ('quantity', models.PositiveIntegerField(default=100)),
            ],
        ),
    ]
