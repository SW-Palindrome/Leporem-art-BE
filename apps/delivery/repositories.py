from apps.delivery.models import DeliveryCompany, DeliveryInfo


class DeliveryRepository:
    def register(self, order_id: int, delivery_company_name: str, invoice_number: str):
        delivery_company = DeliveryCompany.objects.get(name=delivery_company_name)
        return DeliveryInfo.objects.create(
            order_id=order_id,
            delivery_company=delivery_company,
            invoice_number=invoice_number,
        )
