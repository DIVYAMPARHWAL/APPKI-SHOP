# Generated by Django 4.1.7 on 2024-04-16 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0036_passwordresetrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='type',
            field=models.CharField(max_length=100, null=True),
        ),
    ]