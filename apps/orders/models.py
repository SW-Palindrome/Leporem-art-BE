import enum

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_extensions.db.models import TimeStampedModel

from apps.buyers.models import Buyer
from apps.items.models import Item


class OrderStatus(TimeStampedModel):
    class Status(enum.Enum):
        ORDERED = '주문완료'
        DELIVERY_STARTED = '배송중'
        DELIVERED = '배송완료'
        CANCELED = '주문취소'

    order_status_id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=10)

    def get_body(self):
        if self.status == self.Status.ORDERED.value:
            return '주문이 완료되었습니다.'
        elif self.status == self.Status.DELIVERY_STARTED.value:
            return '배송이 시작되었습니다.'
        elif self.status == self.Status.DELIVERED.value:
            return '배송이 완료되었습니다.'
        elif self.status == self.Status.CANCELED.value:
            return '주문이 취소되었습니다.'


class Order(TimeStampedModel):
    order_id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.PROTECT)
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='orders')
    order_status = models.ForeignKey(OrderStatus, on_delete=models.PROTECT)
    price = models.IntegerField()
    ordered_datetime = models.DateTimeField()

    def get_order_status_display(self):
        return self.order_status.status


class OrderHistory(TimeStampedModel):
    order_history_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.PROTECT)


class Review(TimeStampedModel):
    review_id = models.AutoField(primary_key=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='review')
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.CharField(max_length=255)
