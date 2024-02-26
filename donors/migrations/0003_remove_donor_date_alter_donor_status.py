# Generated by Django 4.2.7 on 2024-02-26 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donors", "0002_alter_donor_city_alter_donor_comment_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="donor", name="date",),
        migrations.AlterField(
            model_name="donor",
            name="status",
            field=models.CharField(
                choices=[("Pending", "Pending"), ("Approved", "Approved")],
                default="Pending",
                max_length=124,
            ),
        ),
    ]
