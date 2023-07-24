from django_filters import rest_framework as filters

from apps.orders.models import Order


class SellerMyOrderFilterBackend(filters.FilterSet):
    item_id = filters.CharFilter(field_name='item_id')

    class Meta:
        model = Order
        fields = ['item_id']
