# Generated by Django 4.2 on 2024-03-15 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_dashboard', '0002_alter_generalsetting_created_on_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalsetting',
            name='date_format',
            field=models.CharField(default='dd-mm-yyyy', max_length=254),
        ),
    ]