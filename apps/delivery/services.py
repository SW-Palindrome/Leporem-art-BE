from apps.delivery.repositories import DeliveryRepository
from apps.orders.repositories import OrderRepository


class DeliveryService:
    def register(self, user_id: int, order_id: int, delivery_company_name: str, invoice_number: str):
        if OrderRepository().get_order(order_id).item.seller.user_id != user_id:
            raise ValueError('등록한 작품의 판매자가 아닙니다.')

        return DeliveryRepository().register(
            order_id=order_id,
            delivery_company_name=delivery_company_name,
            invoice_number=invoice_number,
        )
