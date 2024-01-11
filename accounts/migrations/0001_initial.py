# Generated by Django 4.2.7 on 2024-01-10 14:31

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('role_name', models.CharField(choices=[('Normal', 'Normal'), ('Campaign_Approver', 'Campaign_Approver'), ('Campaign_Manager', 'Campaign_Manager'), ('Admin', 'Admin')], max_length=25, unique=True)),
            ],
            options={
                'ordering': ('-created_on',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('is_admin', models.BooleanField(default=False)),
                ('username', models.CharField(max_length=50)),
                ('mobile_number', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('user_type', models.CharField(choices=[('Individual', 'Individual'), ('NGO', 'NGO')], max_length=25)),
                ('accepted_policy', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('user_role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.userrole')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
