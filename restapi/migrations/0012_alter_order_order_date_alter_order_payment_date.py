# Generated by Django 5.0.1 on 2024-01-22 11:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0011_alter_order_order_date_alter_order_payment_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 22, 11, 46, 24, 141235, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 22, 11, 46, 24, 141256, tzinfo=datetime.timezone.utc)),
        ),
    ]
