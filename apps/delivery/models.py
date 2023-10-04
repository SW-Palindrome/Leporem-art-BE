from django.db import models
from django_extensions.db.models import TimeStampedModel

from apps.orders.models import Order


class DeliveryCompany(TimeStampedModel):
    delivery_company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10)


class DeliveryInfo(TimeStampedModel):
    delivery_info_id = models.AutoField(primary_key=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='delivery_info')
    delivery_company = models.ForeignKey(DeliveryCompany, on_delete=models.PROTECT, related_name='delivery_infos')
    invoice_number = models.CharField(max_length=14)
