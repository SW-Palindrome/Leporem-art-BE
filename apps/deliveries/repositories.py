from typing import Optional

from apps.deliveries.models import DeliveryCompany, DeliveryInfo


class DeliveryRepository:
    def register(self, order_id: int, delivery_company_name: str, invoice_number: str):
        delivery_company = DeliveryCompany.objects.get(name=delivery_company_name)
        delivery_info, _ = DeliveryInfo.objects.update_or_create(
            order_id=order_id,
            defaults={
                'delivery_company': delivery_company,
                'invoice_number': invoice_number,
            },
        )
        return delivery_info

    def get_delivery_info(self, order_id: int) -> Optional[DeliveryInfo]:
        try:
            return DeliveryInfo.objects.get(order_id=order_id)
        except DeliveryInfo.DoesNotExist:
            return None
