# Generated by Django 4.2.7 on 2024-01-17 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='campaign',
            old_name='description',
            new_name='story',
        ),
    ]