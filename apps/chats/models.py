import uuid

from django.db import models
from django_extensions.db.models import TimeStampedModel

from apps.buyers.models import Buyer
from apps.sellers.models import Seller
from apps.users.models import User


class ChatRoom(TimeStampedModel):
    chat_room_id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.PROTECT)
    seller = models.ForeignKey(Seller, on_delete=models.PROTECT)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        unique_together = ('buyer', 'seller')

    @property
    def last_message(self):
        return self.messages.order_by('write_datetime').last()


class Message(TimeStampedModel):
    class Type(models.TextChoices):
        TEXT = 'TEXT', '텍스트'
        IMAGE = 'IMAGE', '이미지'
        ITEM_SHARE = 'ITEM_SHARE', '작품 공유'
        ITEM_INQUIRY = 'ITEM_INQUIRY', '작품 문의'
        ORDER = 'ORDER', '주문'

    message_id = models.AutoField(primary_key=True)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.PROTECT, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    write_datetime = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    text = models.CharField(max_length=255)
    image = models.ImageField(upload_to='chats/message_image', null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=20, choices=Type.choices)

    @property
    def message(self):
        type_message_map = {
            self.Type.TEXT.value: self.text,
            self.Type.IMAGE.value: self.image.url if self.image else None,
            self.Type.ITEM_SHARE.value: self.text,
            self.Type.ITEM_INQUIRY.value: self.text,
            self.Type.ORDER.value: self.text,
        }
        return type_message_map[self.type]
