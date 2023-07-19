from django.db import models

from apps.users.models import User


class Buyer(models.Model):
    buyer_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer')

    def __str__(self):
        return f'[Buyer {self.buyer_id}]: {self.user_id}'
