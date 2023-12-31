# Generated by Django 4.2.3 on 2023-07-27 06:37

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('users', '0004_alter_user_profile_image'),
        ('buyers', '0002_alter_buyer_options_buyer_created_buyer_modified'),
        ('sellers', '0003_seller_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                (
                    'created',
                    django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created'),
                ),
                (
                    'modified',
                    django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified'),
                ),
                ('chat_room_id', models.AutoField(primary_key=True, serialize=False)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='buyers.buyer')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sellers.seller')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                (
                    'created',
                    django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created'),
                ),
                (
                    'modified',
                    django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified'),
                ),
                ('message_id', models.AutoField(primary_key=True, serialize=False)),
                ('write_datetime', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('text', models.CharField(max_length=255)),
                ('image', models.ImageField(null=True, upload_to='chats/message_image')),
                (
                    'chat_room',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, related_name='messages', to='chats.chatroom'
                    ),
                ),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.user')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
