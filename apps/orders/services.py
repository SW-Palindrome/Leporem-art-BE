from apps.buyers.respositories import BuyerRepository
from apps.items.repositories import ItemRepository
from apps.orders.exceptions import NotEnoughProductException, SelfOrderException
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
