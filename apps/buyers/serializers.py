from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers


class BuyerInfoSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=20)
    profile_image = serializers.ImageField()
    is_seller = serializers.BooleanField()


class BuyerMyOrderSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    item_id = serializers.IntegerField()
    item_title = serializers.CharField(source='item.title')
    item_thumbnail_image = serializers.CharField(source='item.thumbnail_image.image.url')
    price = serializers.IntegerField()
    ordered_datetime = serializers.DateTimeField()
    order_status = serializers.CharField(source='get_order_status_display')
    is_reviewed = serializers.BooleanField()
    name = serializers.CharField()
    address = serializers.CharField()
    detail_address = serializers.CharField()
    phone_number = PhoneNumberField(region='KR')
    zipcode = serializers.CharField()
