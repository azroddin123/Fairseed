# Generated by Django 4.2 on 2024-01-16 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0005_campaign_campaign_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='country',
            field=models.CharField(blank=True, max_length=124, null=True),
        ),
    ]