from django.db import models


# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    nickname = models.CharField(null=False, max_length=10)
    profile_image = models.CharField(null=True, max_length=250)
    inactive_datetime = models.DateField(auto_now=True)
    is_agree_privacy = models.BooleanField(default=False)
    is_agree_ads = models.BooleanField(default=False)
