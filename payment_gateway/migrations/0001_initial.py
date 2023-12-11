# Generated by Django 4.2.7 on 2023-12-11 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BankTransfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee_percent', models.IntegerField()),
                ('bank_details', models.TextField()),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='PayPal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentage_fee', models.CharField(max_length=124)),
                ('fee_cents', models.CharField(max_length=124)),
                ('paypal_account', models.CharField(max_length=124)),
                ('paypal_sandbox', models.BooleanField(default=False)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PGSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency_code', models.CharField(max_length=50)),
                ('currency_symobl', models.CharField(max_length=10)),
                ('fee_for_donaion', models.IntegerField()),
                ('cuurency_position', models.CharField(max_length=124)),
                ('decimal_format', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='PhonePay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phonepay_key', models.CharField(max_length=154)),
                ('phonepay_secret', models.CharField(max_length=154)),
                ('fee_percent', models.IntegerField()),
                ('fee_cents', models.IntegerField()),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='QRTransfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee_percent', models.IntegerField()),
                ('QR_Path', models.ImageField(blank=True, null=True, upload_to='static/media_files/')),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='RazorPay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razorpay_key', models.BooleanField(max_length=154)),
                ('razorpay_secret', models.BooleanField(max_length=154)),
                ('status', models.BooleanField(default=False)),
                ('fee_percent', models.IntegerField()),
                ('fee_cents', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Stripe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee_percent', models.IntegerField()),
                ('fee_cents', models.IntegerField()),
                ('stripe_public_key', models.CharField(max_length=124)),
                ('stripe_secret_key', models.CharField(max_length=124)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
    ]
