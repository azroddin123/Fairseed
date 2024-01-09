# Generated by Django 4.2.7 on 2024-01-09 09:46

import datetime
from django.db import migrations, models
import django.utils.timezone
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0002_accountdetail_kyc_remove_campaign_start_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='documents',
            name='content',
            field=tinymce.models.HTMLField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='documents',
            name='doc_file',
            field=models.FileField(default=datetime.datetime(2024, 1, 9, 9, 46, 16, 431513, tzinfo=datetime.timezone.utc), upload_to='static/media_files/campaign/documents/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='documents',
            name='doc_name',
            field=models.CharField(blank=True, max_length=124, null=True),
        ),
    ]
