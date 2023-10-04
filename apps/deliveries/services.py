from typing import Optional

from django.conf import settings
from requests import PreparedRequest

from apps.deliveries.repositories import DeliveryRepository
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

    def get_tracking_url(self, user_id: int, order_id: int) -> Optional[str]:
        if OrderRepository().get_order(order_id).buyer.user_id != user_id:
            raise ValueError(f'주문 {order_id}의 신청자가 아닙니다.')

        delivery_info = DeliveryRepository().get_delivery_info(order_id)

        if delivery_info is None:
            return

        request = PreparedRequest()
        query_params = {
            't_key': settings.SMART_DELIVERY_TRACKING_API_KEY,
            't_code': delivery_info.delivery_company.code,
            't_invoice': delivery_info.invoice_number,
        }
        return request.prepare_url(settings.SMART_DELIVERY_TRACKING_API_URL, query_params)
