# Generated by Django 4.2 on 2024-03-16 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donors', '0003_withdrawal'),
    ]

    operations = [
        migrations.AddField(
            model_name='donor',
            name='bank_name',
            field=models.CharField(blank=True, max_length=124, null=True),
        ),
        migrations.AddField(
            model_name='donor',
            name='other_details',
            field=models.CharField(blank=True, max_length=124, null=True),
        ),
        migrations.AddField(
            model_name='donor',
            name='transaction_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]