# Generated by Django 4.2.3 on 2023-07-27 03:34

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):
    dependencies = [
        ('orders', '0002_order_ordered_datetime'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                (
                    'created',
                    django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created'),
                ),
                (
                    'modified',
                    django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified'),
                ),
                ('review_id', models.AutoField(primary_key=True, serialize=False)),
                (
                    'rating',
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(5),
                        ]
                    ),
                ),
                ('comment', models.CharField(max_length=255)),
                (
                    'order',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, related_name='review', to='orders.order'
                    ),
                ),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]