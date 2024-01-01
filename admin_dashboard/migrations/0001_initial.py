# Generated by Django 3.2 on 2024-01-01 04:55
# Generated by Django 4.2.7 on 2023-12-27 05:53

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralSetting',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('namesite', models.CharField(max_length=32)),
                ('welcome_text', models.CharField(max_length=32)),
                ('welcome_subtitle', models.CharField(max_length=32)),
                ('description', models.CharField(max_length=124)),
                ('email_admin', models.EmailField(max_length=254)),
                ('tandc_url', models.CharField(max_length=254)),
                ('privacy_policy_url', models.CharField(max_length=254)),
                ('email_no_reply', models.CharField(max_length=124)),
                ('new_registration', models.BooleanField(default=True)),
                ('auto_approve', models.BooleanField(default=False)),
                ('email_verification', models.BooleanField(default=False)),
                ('facebook_login', models.BooleanField(default=False)),
                ('google_login', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-created_on',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LandingPage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='static/media_files/')),
                ('logo_footer', models.ImageField(blank=True, null=True, upload_to='static/media_files/')),
                ('favicon', models.ImageField(blank=True, null=True, upload_to='static/media_files/')),
                ('image_header', models.ImageField(blank=True, null=True, upload_to='static/media_files/')),
                ('image_bottom', models.ImageField(blank=True, null=True, upload_to='static/media_files/')),
                ('avtar', models.ImageField(blank=True, null=True, upload_to='static/media_files/')),
                ('image_category', models.ImageField(blank=True, null=True, upload_to='static/media_files/')),
                ('default_link_color', models.CharField(max_length=45)),
            ],
            options={
                'ordering': ('-created_on',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Limit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('num_campaigns', models.PositiveIntegerField()),
                ('file_size', models.PositiveIntegerField()),
                ('campaign_min_amount', models.PositiveIntegerField()),
                ('campaign_max_amount', models.PositiveIntegerField()),
                ('donation_min_amount', models.PositiveIntegerField()),
                ('donation_max_amount', models.PositiveIntegerField()),
                ('max_donation_amount', models.PositiveIntegerField()),
            ],
            options={
                'ordering': ('-created_on',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pages',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=50)),
                ('slug', models.CharField(max_length=124)),
                ('show_navbar', models.BooleanField(default=False)),
                ('show_footer', models.BooleanField(default=True)),
                ('show_page', models.BooleanField(default=True)),
                ('content', models.TextField()),
            ],
            options={
                'ordering': ('-created_on',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SocialProfile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('facebook_url', models.CharField(max_length=124)),
                ('twitter_url', models.CharField(max_length=124)),
                ('instagram_url', models.CharField(max_length=124)),
            ],
            options={
                'ordering': ('-created_on',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('gs', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_dashboard.generalsetting')),
            ],
            options={
                'ordering': ('-created_on',),
                'abstract': False,
            },
        ),
    ]
