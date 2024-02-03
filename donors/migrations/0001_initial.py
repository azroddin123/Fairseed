# Generated by Django 4.2.7 on 2024-02-03 12:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('campaigns', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('donation_type', models.CharField(choices=[('General_Donation', 'General_Donation'), ('Zakat', 'Zakat'), ('Interest_Offloading', 'Interest_Offloading')], max_length=124)),
                ('full_name', models.CharField(max_length=124)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('email', models.CharField(max_length=124)),
                ('city', models.CharField(max_length=124)),
                ('country', models.CharField(max_length=124)),
                ('mobile', models.CharField(max_length=124)),
                ('pancard', models.CharField(blank=True, max_length=124, null=True)),
                ('comment', models.TextField()),
                ('date', models.DateField(blank=True, null=True)),
                ('payment_type', models.CharField(choices=[('Bank_Transfer', 'Bank_Transfer'), ('UPI', 'UPI')], max_length=124)),
                ('is_anonymous', models.BooleanField(default=False)),
                ('status', models.BooleanField(default=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donors', to='campaigns.campaign')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_on',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UpiTransaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('signature', models.CharField(max_length=200)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('donor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='upi_transaction', to='donors.donor')),
            ],
            options={
                'ordering': ('-created_on',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BankTransaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('transaction_id', models.CharField(max_length=124)),
                ('bank_name', models.CharField(max_length=124)),
                ('transaction_date', models.DateField()),
                ('other_details', models.CharField(blank=True, max_length=124, null=True)),
                ('donor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bank_transaction', to='donors.donor')),
            ],
            options={
                'ordering': ('-created_on',),
                'abstract': False,
            },
        ),
    ]
