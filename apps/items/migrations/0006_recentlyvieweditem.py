# Generated by Django 4.2.3 on 2023-07-31 06:03

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):
    dependencies = [
        ('buyers', '0002_alter_buyer_options_buyer_created_buyer_modified'),
        ('items', '0005_like_buyer_alter_category_category_alter_color_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecentlyViewedItem',
            fields=[
                (
                    'created',
                    django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created'),
                ),
                (
                    'modified',
                    django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified'),
                ),
                ('recently_viewed_item_id', models.AutoField(primary_key=True, serialize=False)),
                ('viewed_date', models.DateTimeField(auto_now_add=True)),
                ('deleted_date', models.DateTimeField()),
                (
                    'buyer',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='recently_viewed_items',
                        to='buyers.buyer',
                    ),
                ),
                (
                    'item',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='recently_viewed_items',
                        to='items.item',
                    ),
                ),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
