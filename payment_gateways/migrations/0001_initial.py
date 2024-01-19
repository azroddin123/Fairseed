# Generated by Django 4.2.7 on 2024-01-18 12:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BankTransfer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('fee_percent', models.IntegerField()),
                ('bank_details', models.TextField()),
                ('is_enabled', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('-created_on',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PayPal',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('percentage_fee', models.CharField(max_length=124)),
                ('fee_cents', models.CharField(max_length=124)),
                ('paypal_account', models.CharField(max_length=124)),
                ('paypal_sandbox', models.BooleanField(default=False)),
                ('is_enabled', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-created_on',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PGSetting',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('currency_code', models.CharField(max_length=50)),
                ('currency_symbol', models.CharField(max_length=10)),
                ('fee_for_donation', models.IntegerField()),
                ('currency_position', models.CharField(max_length=124)),
                ('decimal_format', models.CharField(max_length=124)),
            ],
            options={
                'ordering': ('-created_on',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PhonePay',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('phonepay_key', models.CharField(max_length=154)),
                ('phonepay_secret', models.CharField(max_length=154)),
                ('fee_percent', models.IntegerField()),
                ('fee_cents', models.IntegerField()),
                ('is_enabled', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-created_on',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='QRTransfer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('fee_percent', models.IntegerField()),
                ('qr_path', models.ImageField(blank=True, null=True, upload_to='')),
                ('is_enabled', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-created_on',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RazorPay',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('razorpay_key', models.CharField(max_length=154)),
                ('razorpay_secret', models.CharField(max_length=154)),
                ('is_enabled', models.BooleanField(default=False)),
                ('fee_percent', models.IntegerField()),
                ('fee_cents', models.IntegerField()),
            ],
            options={
                'ordering': ('-created_on',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Stripe',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('fee_percent', models.IntegerField()),
                ('fee_cents', models.IntegerField()),
                ('stripe_public_key', models.CharField(max_length=124)),
                ('stripe_secret_key', models.CharField(max_length=124)),
                ('is_enabled', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-created_on',),
                'abstract': False,
            },
        ),
    ]
