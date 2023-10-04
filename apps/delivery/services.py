from apps.delivery.repositories import DeliveryRepository


class DeliveryService:
    def register(self, order_id: int, delivery_company_name: str, invoice_number: str):
        return DeliveryRepository().register(
            order_id=order_id,
            delivery_company_name=delivery_company_name,
            invoice_number=invoice_number,
        )
