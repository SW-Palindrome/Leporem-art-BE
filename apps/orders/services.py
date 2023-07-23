from apps.buyers.respositories import BuyerRepository
from apps.items.repositories import ItemRepository
from apps.orders.exceptions import (
    InvalidOrderStatusException,
    NotEnoughProductException,
    SelfOrderException,
)
from apps.orders.models import OrderStatus
from apps.orders.repositories import OrderRepository


class OrderService:
    def order(self, buyer_id, item_id):
        item = ItemRepository().get_item(item_id)
        buyer = BuyerRepository().get_buyer(buyer_id)

        if item.seller.user_id == buyer.user_id:
            raise SelfOrderException('자신의 상품은 주문할 수 없습니다.')

        if item.current_amount <= 0:
            raise NotEnoughProductException('재고가 없습니다.')

        return OrderRepository().order(buyer_id, item_id)

    def start_delivery(self, order_id):
        order = OrderRepository().get_order(order_id)
        if order.order_status.status != OrderStatus.Status.ORDERED.value:
            raise InvalidOrderStatusException('주문 완료 상태에서만 배송이 가능합니다.')

        return OrderRepository().start_delivery(order_id)

    def complete_delivery(self, order_id):
        order = OrderRepository().get_order(order_id)
        if order.order_status.status != OrderStatus.Status.DELIVERY_STARTED.value:
            raise InvalidOrderStatusException('배송중 상태에서만 배송 완료가 가능합니다.')

        return OrderRepository().complete_delivery(order_id)

    def cancel(self, order_id):
        order = OrderRepository().get_order(order_id)
        if order.order_status.status not in [
            OrderStatus.Status.ORDERED.value,
            OrderStatus.Status.DELIVERY_STARTED.value,
        ]:
            raise InvalidOrderStatusException('주문 완료 및 배송중 상태에서만 주문 취소가 가능합니다.')

        return OrderRepository().cancel(order_id)
