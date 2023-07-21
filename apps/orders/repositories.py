from apps.items.models import Item
from apps.orders.models import Order, OrderStatus


class OrderRepository:
    def order(self, buyer_id, item_id):
        item = Item.objects.get(item_id=item_id)
        Order.objects.create(
            buyer_id=buyer_id,
            item=item,
            order_status=OrderStatus.objects.get(status=OrderStatus.Status.ORDERED.value),
            price=item.price,
        )
