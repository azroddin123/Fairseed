# Generated by Django 4.2 on 2024-01-16 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0006_campaign_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='country',
        ),
    ]
