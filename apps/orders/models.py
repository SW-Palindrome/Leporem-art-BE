import enum

from django.db import models
from django_extensions.db.models import TimeStampedModel

from apps.buyers.models import Buyer
from apps.items.models import Item


class OrderStatus(TimeStampedModel):
    class Status(enum.Enum):
        ORDERED = '주문완료'
        PAYMENT_COMPLETED = '배송중'
        DELIVERED = '배송완료'
        CANCELED = '주문취소'

    order_status_id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=10)


class Order(TimeStampedModel):
    order_id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.PROTECT)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.PROTECT)
    price = models.IntegerField()


class OrderHistory(TimeStampedModel):
    order_history_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.PROTECT)
