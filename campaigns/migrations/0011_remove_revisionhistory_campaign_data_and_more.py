# Generated by Django 4.2 on 2024-03-20 06:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0010_rename_modeified_by_revisionhistory_modified_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='revisionhistory',
            name='campaign_data',
        ),
        migrations.AddField(
            model_name='revisionhistory',
            name='cause_data',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='campaigns.causeedit'),
        ),
    ]
