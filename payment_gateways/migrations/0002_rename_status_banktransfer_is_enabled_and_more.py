# Generated by Django 4.2.7 on 2023-12-27 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment_gateways', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='banktransfer',
            old_name='status',
            new_name='is_enabled',
        ),
        migrations.RenameField(
            model_name='paypal',
            old_name='status',
            new_name='is_enabled',
        ),
        migrations.RenameField(
            model_name='phonepay',
            old_name='status',
            new_name='is_enabled',
        ),
        migrations.RenameField(
            model_name='qrtransfer',
            old_name='status',
            new_name='is_enabled',
        ),
        migrations.RenameField(
            model_name='razorpay',
            old_name='status',
            new_name='is_enabled',
        ),
        migrations.RenameField(
            model_name='stripe',
            old_name='status',
            new_name='is_enabled',
        ),
    ]
