from apps.orders.repositories import OrderRepository


class OrderService:
    def order(self, buyer_id, item_id):
        return OrderRepository().order(buyer_id, item_id)
