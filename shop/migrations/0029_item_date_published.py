# Generated by Django 4.1.7 on 2023-04-07 05:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0028_remove_order_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='date_published',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 7, 5, 6, 57, 905040, tzinfo=datetime.timezone.utc)),
        ),
    ]
