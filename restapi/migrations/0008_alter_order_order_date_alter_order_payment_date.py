# Generated by Django 5.0.1 on 2024-01-22 11:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0007_alter_order_order_date_alter_order_payment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 22, 11, 40, 36, 578636, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 22, 11, 40, 36, 578649, tzinfo=datetime.timezone.utc)),
        ),
    ]
