# Generated by Django 4.2.3 on 2023-10-25 06:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('orders', '0007_order_detail_address_alter_order_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]
