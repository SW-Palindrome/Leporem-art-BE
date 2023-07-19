from rest_framework import serializers


class BuyerInfoSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=20)
    profile_image = serializers.ImageField()
    is_seller = serializers.BooleanField()
