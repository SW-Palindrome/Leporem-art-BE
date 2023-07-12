# Generated by Django 4.2.3 on 2023-07-12 08:16

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('sellers', '0002_alter_verifyemail_verify_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                (
                    'created',
                    django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created'),
                ),
                (
                    'modified',
                    django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified'),
                ),
                ('item_id', models.AutoField(primary_key=True, serialize=False)),
                ('price', models.IntegerField(null=True)),
                ('max_amount', models.IntegerField()),
                ('current_amount', models.IntegerField()),
                ('title', models.CharField(max_length=46)),
                ('description', models.CharField(max_length=255, null=True)),
                ('shorts', models.FileField(upload_to='items/item_shorts/')),
                ('width', models.DecimalField(decimal_places=2, max_digits=6)),
                ('depth', models.DecimalField(decimal_places=2, max_digits=6)),
                ('height', models.DecimalField(decimal_places=2, max_digits=6)),
                ('display_dt', models.DateTimeField(null=True)),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ItemImage',
            fields=[
                (
                    'created',
                    django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created'),
                ),
                (
                    'modified',
                    django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified'),
                ),
                ('item_image_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_thumbnail', models.BooleanField(default=False)),
                ('image', models.FileField(upload_to='items/item_image/')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ItemTagMapping',
            fields=[
                (
                    'created',
                    django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created'),
                ),
                (
                    'modified',
                    django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified'),
                ),
                ('item_tag_mapping_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                (
                    'created',
                    django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created'),
                ),
                (
                    'modified',
                    django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified'),
                ),
                ('tag_id', models.AutoField(primary_key=True, serialize=False)),
                ('category', models.CharField(max_length=10)),
                ('color', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddConstraint(
            model_name='tag',
            constraint=models.UniqueConstraint(fields=('category', 'color'), name='unique together'),
        ),
        migrations.AddField(
            model_name='itemtagmapping',
            name='item',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name='item_tag_mappings', to='items.item'
            ),
        ),
        migrations.AddField(
            model_name='itemtagmapping',
            name='tag',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name='item_tag_mappings', to='items.tag'
            ),
        ),
        migrations.AddField(
            model_name='itemimage',
            name='item',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name='item_images', to='items.item'
            ),
        ),
        migrations.AddField(
            model_name='item',
            name='seller',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name='items', to='sellers.seller'
            ),
        ),
    ]
