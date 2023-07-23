from django.db import transaction

from apps.items.models import Item
from apps.orders.models import Order, OrderHistory, OrderStatus


class OrderRepository:
    @transaction.atomic
    def order(self, buyer_id, item_id):
        item = Item.objects.get(item_id=item_id)
        order_status = OrderStatus.objects.get(status=OrderStatus.Status.ORDERED.value)
        order = Order.objects.create(
            buyer_id=buyer_id,
            item=item,
            order_status=order_status,
            price=item.price,
        )
        OrderHistory.objects.create(
            order=order,
            order_status=order_status,
        )
        item.current_amount -= 1
        item.save()
