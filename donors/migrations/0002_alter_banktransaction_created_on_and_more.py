# Generated by Django 4.2 on 2024-03-09 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donors', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banktransaction',
            name='created_on',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='banktransaction',
            name='updated_on',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='donor',
            name='created_on',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='donor',
            name='updated_on',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='upitransaction',
            name='created_on',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='upitransaction',
            name='updated_on',
            field=models.DateField(auto_now=True),
        ),
    ]