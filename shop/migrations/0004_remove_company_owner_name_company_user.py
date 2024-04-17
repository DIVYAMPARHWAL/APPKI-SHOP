# Generated by Django 4.1.7 on 2023-03-26 08:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0003_address_payment_orderitem_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='owner_name',
        ),
        migrations.AddField(
            model_name='company',
            name='user',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
