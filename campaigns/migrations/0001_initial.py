# Generated by Django 4.2 on 2023-12-21 10:49

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('rasing_for', models.CharField(choices=[('Self', 'Self'), ('Other', 'Other')], max_length=124)),
                ('title', models.CharField(max_length=50)),
                ('goal_amount', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(100, message='Value must be greater than or equal to 100'), django.core.validators.MaxValueValidator(1000000, message='Value must be less than or equal to 1000000')])),
                ('fund_raised', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0, message='Value must be greater than or equal to 0'), django.core.validators.MaxValueValidator(100000, message='Value must be less than or equal to 100000')])),
                ('location', models.CharField(max_length=124)),
                ('zakat_eligible', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='Yes', max_length=124)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Active', 'Active'), ('Completed', 'Completed'), ('Rejected', 'Rejected')], default='Pending', max_length=124)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('description', models.TextField()),
                ('summary', models.TextField()),
                ('is_successfull', models.BooleanField(default=False)),
                ('is_featured', models.BooleanField(default=False)),
                ('is_reported', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-created_on',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CampaignCatagory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('image', models.ImageField(blank=True, null=True, upload_to='static/media_files/')),
                ('status', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-created_on',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('doc_name', models.CharField(max_length=124)),
                ('doc_file', models.FileField(blank=True, null=True, upload_to='static/media_files/')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='campaigns.campaign')),
            ],
            options={
                'ordering': ('-created_on',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CampaignKycBenificiary',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('account_holder_name', models.CharField(max_length=124)),
                ('account_number', models.PositiveIntegerField()),
                ('bank_name', models.CharField(max_length=124)),
                ('branch_name', models.CharField(max_length=124)),
                ('ifsc_code', models.CharField(max_length=124)),
                ('passbook_image', models.ImageField(blank=True, null=True, upload_to='static/media_files/')),
                ('pan_card', models.CharField(max_length=10)),
                ('pan_card_image', models.ImageField(blank=True, null=True, upload_to='static/media_files/')),
                ('adhar_card', models.CharField(max_length=16)),
                ('adhar_card_image', models.ImageField(blank=True, null=True, upload_to='static/media_files/')),
                ('other_details', models.CharField(blank=True, max_length=100, null=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('campaign', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bank_details', to='campaigns.campaign')),
            ],
            options={
                'ordering': ('-created_on',),
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='campaign',
            name='catagory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campaigns.campaigncatagory'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
