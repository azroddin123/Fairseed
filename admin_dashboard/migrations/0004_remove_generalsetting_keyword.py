# Generated by Django 4.2.7 on 2024-01-05 06:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_dashboard', '0003_rename_file_size_limit_max_file_size_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='generalsetting',
            name='Keyword',
        ),
    ]