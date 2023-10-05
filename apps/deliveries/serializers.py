from rest_framework import serializers


class RegisterDeliveryInfoSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    delivery_company = serializers.CharField(max_length=20)
    invoice_number = serializers.CharField(max_length=14)
