from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers


class OrderInfoSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    item_id = serializers.IntegerField()
    item_title = serializers.CharField(source='item.title')
    item_thumbnail_image = serializers.CharField(source='item.thumbnail_image.image.url')
    price = serializers.IntegerField()
    ordered_datetime = serializers.DateTimeField()
    order_status = serializers.CharField(source='get_order_status_display')
    seller_nickname = serializers.CharField(source='item.seller.user.nickname')


class OrderSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()


class ReviewSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    rating = serializers.IntegerField()
    comment = serializers.CharField(required=False)


class OrderSerializerV1(serializers.Serializer):
    item_id = serializers.IntegerField()
    name = serializers.CharField()
    address = serializers.CharField()
    phone_number = PhoneNumberField(region='KR')
    zipcode = serializers.CharField()
