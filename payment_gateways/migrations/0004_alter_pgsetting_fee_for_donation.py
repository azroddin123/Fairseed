# Generated by Django 4.2 on 2024-02-04 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_gateways', '0003_alter_pgsetting_currency_position_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pgsetting',
            name='fee_for_donation',
            field=models.CharField(choices=[('0%', '0%'), ('1%', '1%'), ('2%', '2%'), ('3%', '3%'), ('4%', '4%'), ('5%', '5%'), ('6%', '6%'), ('7%', '7%'), ('8%', '8%'), ('9%', '9%'), ('10%', '10%'), ('15%', '15%')], max_length=5),
        ),
    ]
