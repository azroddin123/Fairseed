# Generated by Django 4.2 on 2024-01-20 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_user_confirm_password_user_new_password_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='static/media_files/campaign_images/'),
        ),
    ]