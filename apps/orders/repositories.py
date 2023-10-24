from django.db import transaction
from django.db.models import Exists, OuterRef
from django.utils import timezone

from apps.items.models import Item
from apps.orders.models import Order, OrderHistory, OrderStatus, Review


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
            ordered_datetime=timezone.now(),
        )
        OrderHistory.objects.create(
            order=order,
            order_status=order_status,
        )
        item.current_amount -= 1
        item.save()
        return order

    def get_order(self, order_id):
        return Order.objects.get(order_id=order_id)

    @transaction.atomic
    def start_delivery(self, order_id):
        order = Order.objects.get(order_id=order_id)
        order_status = OrderStatus.objects.get(status=OrderStatus.Status.DELIVERY_STARTED.value)
        order.order_status = order_status
        order.save()
        OrderHistory.objects.create(
            order=order,
            order_status=order_status,
        )

    @transaction.atomic
    def complete_delivery(self, order_id):
        order = Order.objects.get(order_id=order_id)
        order_status = OrderStatus.objects.get(status=OrderStatus.Status.DELIVERED.value)
        order.order_status = order_status
        order.save()
        OrderHistory.objects.create(
            order=order,
            order_status=order_status,
        )

    @transaction.atomic
    def cancel(self, order_id):
        order = Order.objects.get(order_id=order_id)
        order_status = OrderStatus.objects.get(status=OrderStatus.Status.CANCELED.value)
        order.order_status = order_status
        order.save()
        OrderHistory.objects.create(
            order=order,
            order_status=order_status,
        )
        item = order.item
        item.current_amount += 1
        item.save()

    def get_order_list_by_seller(self, seller_id):
        return (
            Order.objects.filter(item__seller_id=seller_id)
            .select_related('item', 'buyer__user', 'order_status')
            .order_by('-ordered_datetime')
        )

    def get_order_list_by_buyer(self, buyer_id):
        return (
            Order.objects.filter(buyer_id=buyer_id)
            .select_related('item', 'order_status')
            .annotate(is_reviewed=Exists(Review.objects.filter(order=OuterRef('pk'))))
            .order_by('-ordered_datetime')
        )

    @transaction.atomic
    def order_v1(self, buyer_id, item_id, name, address, phone_number, zipcode):
        item = Item.objects.get(item_id=item_id)
        order_status = OrderStatus.objects.get(status=OrderStatus.Status.ORDERED.value)
        order = Order.objects.create(
            buyer_id=buyer_id,
            item=item,
            order_status=order_status,
            price=item.price,
            ordered_datetime=timezone.now(),
            name=name,
            address=address,
            phone_number=phone_number,
            zipcode=zipcode,
        )
        OrderHistory.objects.create(
            order=order,
            order_status=order_status,
        )
        item.current_amount -= 1
        item.save()
        return order


class ReviewRepository:
    @transaction.atomic
    def register(self, order_id, rating, comment):
        order_id = Order.objects.get(pk=order_id)
        return Review.objects.create(order=order_id, rating=rating, comment=comment)

    def get_order(self, order_id):
        return Review.objects.get(order=order_id)
