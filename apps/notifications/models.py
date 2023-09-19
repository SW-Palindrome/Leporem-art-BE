from django.db import models
from django_extensions.db.models import TimeStampedModel

from apps.users.models import User


class Device(TimeStampedModel):
    device_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='devices', null=True)
    fcm_token = models.CharField(max_length=255, unique=True)
