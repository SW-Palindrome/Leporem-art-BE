# Generated by Django 4.2.3 on 2023-08-06 09:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0004_alter_user_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='useroauthinfo',
            name='refresh_token',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
