# Generated by Django 4.2.3 on 2023-07-27 05:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('sellers', '0003_seller_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='temperature',
            field=models.FloatField(default=0, null=True),
        ),
    ]