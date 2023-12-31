# Generated by Django 4.2.3 on 2023-07-31 06:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('items', '0006_recentlyvieweditem'),
        ('items', '0005_like_buyer_alter_category_category_alter_color_color'),
        ('orders', '0003_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='item',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='items.item'
            ),
        ),
    ]
