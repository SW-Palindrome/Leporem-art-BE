from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils import timezone


class User(AbstractBaseUser):
    user_id = models.UUIDField(primary_key=True, editable=False)
    nickname = models.CharField(max_length=20, unique=True)
    profile_image = models.CharField(max_length=50, null=True)
    inactive_datetime = models.DateTimeField(null=True)
    is_agree_privacy = models.BooleanField(default=False)
    is_agree_ads = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    age_range = models.PositiveIntegerField(null=True)
    gender = models.CharField(null=True, max_length=2)
    is_seller = models.BooleanField(null=False)
    is_staff = models.BooleanField(null=False)
    created_date = models.DateTimeField(default=timezone.now)
    created_no = models.PositiveIntegerField(null=False)
    modified_date = models.DateTimeField(auto_now=True)
    modified_no = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'nickname'


class UserOAuthInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.CharField(max_length=20)
    provider_id = models.CharField(max_length=100)

    class Meta:
        unique_together = ('provider', 'provider_id')
