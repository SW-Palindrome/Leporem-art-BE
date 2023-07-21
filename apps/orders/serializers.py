from rest_framework import serializers


class OrderSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
