from rest_framework import serializers


class OrderSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()


class ReviewSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    rating = serializers.IntegerField()
    comment = serializers.CharField(required=False)
