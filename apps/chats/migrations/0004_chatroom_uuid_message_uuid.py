# Generated by Django 4.2.3 on 2023-08-05 16:09

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ('chats', '0003_alter_chatroom_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name='message',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
