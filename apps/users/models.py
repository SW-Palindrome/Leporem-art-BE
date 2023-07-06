from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils import timezone
from django_extensions.db.models import TimeStampedModel


class User(AbstractBaseUser, TimeStampedModel):
    user_id = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=20, unique=True)
    profile_image = models.CharField(max_length=50, null=True)
    inactive_datetime = models.DateTimeField(null=True)
    is_agree_privacy = models.BooleanField(default=False)
    is_agree_ads = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'nickname'


class UserOAuthInfo(TimeStampedModel):
    user_oauth_info_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.CharField(max_length=20)
    provider_id = models.CharField(max_length=50)
    access_token = models.CharField(max_length=50)
    refresh_token = models.CharField(max_length=50)
    expiry_datetime = models.DateTimeField()



    class Meta:
        unique_together = ('provider', 'provider_id')
