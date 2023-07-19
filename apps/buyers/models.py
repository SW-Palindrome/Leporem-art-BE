from django.db import models
from django_extensions.db.models import TimeStampedModel

from apps.users.models import User


class Buyer(TimeStampedModel):
    buyer_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer')

    def __str__(self):
        return f'[Buyer {self.buyer_id}]: {self.user_id}'
