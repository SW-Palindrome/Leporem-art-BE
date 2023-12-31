# Generated by Django 4.2.3 on 2023-10-26 06:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('items', '0011_item_end_date_item_start_date'),
        ('exhibitions', '0009_merge_20231025_1327'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exhibitionitem',
            options={},
        ),
        migrations.AlterField(
            model_name='exhibitionitem',
            name='item',
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='exhibition_item',
                to='items.item',
            ),
        ),
        migrations.AlterUniqueTogether(
            name='exhibitionitem',
            unique_together={('exhibition', 'position')},
        ),
    ]
