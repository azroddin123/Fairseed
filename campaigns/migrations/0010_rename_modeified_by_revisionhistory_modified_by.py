# Generated by Django 4.2 on 2024-03-20 05:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0009_rename_adhar_card_image_bankkycedit_adhar_image_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='revisionhistory',
            old_name='modeified_by',
            new_name='modified_by',
        ),
    ]
