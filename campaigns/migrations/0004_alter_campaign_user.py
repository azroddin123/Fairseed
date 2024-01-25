# Generated by Django 3.2 on 2024-01-10 05:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_otp'),
        ('campaigns', '0003_rename_is_successfull_campaign_is_successful_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user'),
        ),
    ]