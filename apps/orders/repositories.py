from apps.orders.models import Order, OrderStatus


class OrderRepository:
    def order(self, buyer_id, item_id):
        Order.objects.create(
            buyer_id=buyer_id,
            item_id=item_id,
            order_status=OrderStatus.objects.get(status=OrderStatus.Status.ORDERED.value),
        )
