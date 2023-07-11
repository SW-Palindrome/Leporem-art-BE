from django.db import models
from django_extensions.db.models import TimeStampedModel

from apps.users.models import User


class Seller(TimeStampedModel):
    seller_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller')
    email = models.EmailField(max_length=50, unique=True)
    temperature = models.FloatField(null=True)

    def __str__(self):
        return f'[Seller {self.seller_id}]: {self.email}'


class VerifyEmail(TimeStampedModel):
    verify_email_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verify_email')
    email = models.EmailField(max_length=50)
    verify_code = models.CharField(max_length=6)
