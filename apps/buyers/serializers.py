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
