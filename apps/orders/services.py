from apps.buyers.respositories import BuyerRepository
from apps.items.repositories import ItemRepository
from apps.orders.exceptions import (
    IntegrityOrderIDException,
    InvalidOrderIDException,
    InvalidOrderStatusException,
    InvalidOrderStatusReviewException,
    NotEnoughProductException,
    OrderPermissionException,
    SelfOrderException,
)
from apps.orders.models import Order, OrderStatus, Review
from apps.orders.repositories import OrderRepository, ReviewRepository


class OrderService:
    def get_order_info(self, order_id, user_id):
        order = OrderRepository().get_order(order_id)
        if user_id not in [order.buyer.user_id, order.item.seller.user_id]:
            raise OrderPermissionException('주문자 혹은 판매자가 아닙니다.')
        return order

    def order(self, buyer_id, item_id):
        item = ItemRepository().get_item(item_id)
        buyer = BuyerRepository().get_buyer(buyer_id)

        if item.seller.user_id == buyer.user_id:
            raise SelfOrderException('자신의 상품은 주문할 수 없습니다.')

        if item.current_amount <= 0:
            raise NotEnoughProductException('재고가 없습니다.')

        return OrderRepository().order(buyer_id, item_id)

    def start_delivery(self, seller_id, order_id):
        order = OrderRepository().get_order(order_id)

        if order.item.seller_id != seller_id:
            raise OrderPermissionException('판매자가 아닙니다.')

        if order.order_status.status != OrderStatus.Status.ORDERED.value:
            raise InvalidOrderStatusException('주문 완료 상태에서만 배송이 가능합니다.')

        return OrderRepository().start_delivery(order_id)

    def complete_delivery(self, seller_id, order_id):
        order = OrderRepository().get_order(order_id)

        if order.item.seller_id != seller_id:
            raise OrderPermissionException('판매자가 아닙니다.')

        if order.order_status.status != OrderStatus.Status.DELIVERY_STARTED.value:
            raise InvalidOrderStatusException('배송중 상태에서만 배송 완료가 가능합니다.')

        return OrderRepository().complete_delivery(order_id)

    def cancel(self, user_id, order_id):
        order = OrderRepository().get_order(order_id)

        if order.item.seller.user_id != user_id and order.buyer.user_id != user_id:
            raise OrderPermissionException('판매자 혹은 구매자가 아닙니다.')

        if order.order_status.status not in [
            OrderStatus.Status.ORDERED.value,
        ]:
            raise InvalidOrderStatusException('주문 완료 상태에서만 주문 취소가 가능합니다.')

        return OrderRepository().cancel(order_id)


class ReviewService:
    def register(self, order_id, rating, comment):
        try:
            order = OrderRepository().get_order(order_id)
        except Order.DoesNotExist:
            raise InvalidOrderIDException("Order does not exist.")

        if order.order_status.status != OrderStatus.Status.DELIVERED.value:
            raise InvalidOrderStatusReviewException("Review can only be submitted in the 'DELIVERED' status.")

        try:
            ReviewRepository().get_order(order_id)
            raise IntegrityOrderIDException("Duplicate entry for order_id.")
        except Review.DoesNotExist:
            None

        return ReviewRepository().register(order_id, rating, comment)
