# Generated by Django 3.2 on 2023-12-12 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0006_campaign_is_successfull'),
    ]

    operations = [
        migrations.RenameField(
            model_name='campaign',
            old_name='is_features',
            new_name='is_featured',
        ),
    ]
