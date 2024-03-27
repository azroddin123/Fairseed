# Generated by Django 4.2 on 2024-03-18 23:02

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0002_alter_bankkyc_bank_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='CauseEdit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('updated_on', models.DateField(auto_now=True)),
                ('campaign_data', models.JSONField(blank=True, default=dict, null=True)),
                ('campaign_image', models.ImageField(upload_to='')),
                ('document_image', models.ImageField(upload_to='')),
                ('approval_status', models.CharField(choices=[('No_Request', 'No_Request'), ('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='No_Request', max_length=240)),
                ('campaign', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='campaigns.campaign')),
            ],
            options={
                'ordering': ('-created_on',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BankKYCEdit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('updated_on', models.DateField(auto_now=True)),
                ('bank_data', models.JSONField(default=dict)),
                ('approval_status', models.CharField(choices=[('No_Request', 'No_Request'), ('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='No_Request', max_length=240)),
                ('bank_kyc', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='campaigns.bankkyc')),
            ],
            options={
                'ordering': ('-created_on',),
                'abstract': False,
            },
        ),
    ]