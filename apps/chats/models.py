from django.db import models
from django_extensions.db.models import TimeStampedModel

from apps.buyers.models import Buyer
from apps.sellers.models import Seller
from apps.users.models import User


class ChatRoom(TimeStampedModel):
    chat_room_id = models.AutoField(primary_key=True)
    buyer_id = models.ForeignKey(Buyer, on_delete=models.PROTECT)
    seller_id = models.ForeignKey(Seller, on_delete=models.PROTECT)


class Message(TimeStampedModel):
    message_id = models.AutoField(primary_key=True)
    chat_room_id = models.ForeignKey(ChatRoom, on_delete=models.PROTECT, related_name='messages')
    sender_id = models.ForeignKey(User, on_delete=models.PROTECT)
    write_datetime = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    text = models.CharField(max_length=255)
    image = models.ImageField(upload_to='chats/message_image', null=True)
