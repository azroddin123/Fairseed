# Generated by Django 4.2.7 on 2024-01-10 07:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0004_alter_documents_campaign_alter_documents_doc_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documents',
            name='content',
        ),
        migrations.RemoveField(
            model_name='documents',
            name='doc_name',
        ),
    ]
