from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils import timezone
from django_extensions.db.models import TimeStampedModel


class User(AbstractBaseUser, TimeStampedModel):
    user_id = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=20, unique=True)
    profile_image = models.ImageField(upload_to='user/profile_images/', null=True)
    inactive_datetime = models.DateTimeField(null=True)
    is_agree_privacy = models.BooleanField(default=False)
    is_agree_ads = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    is_seller = models.BooleanField(null=False)
    is_staff = models.BooleanField(null=False)
    USERNAME_FIELD = 'nickname'

    def __str__(self):
        return f'[User {self.user_id}]: {self.nickname}'


class UserOAuthInfo(TimeStampedModel):
    user_oauth_info_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_oauth_info')
    provider = models.CharField(max_length=20)
    provider_id = models.CharField(max_length=50)

    class Meta:
        unique_together = ('provider', 'provider_id')
