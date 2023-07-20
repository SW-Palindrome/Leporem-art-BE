from rest_framework import serializers


class SellerRegisterSerializer(serializers.Serializer):
    email = serializers.RegexField(r'^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9-]+\.)+ac\.kr$')


class SellerVerifySerializer(serializers.Serializer):
    verify_code = serializers.CharField(max_length=6)


class SellerItemSerializer(serializers.Serializer):
    price = serializers.IntegerField()
    max_amount = serializers.IntegerField()
    title = serializers.CharField(max_length=46)
    description = serializers.CharField(max_length=255)
    shorts = serializers.FileField()
    width = serializers.DecimalField(max_digits=6, decimal_places=2)
    depth = serializers.DecimalField(max_digits=6, decimal_places=2)
    height = serializers.DecimalField(max_digits=6, decimal_places=2)
    thumbnail_image = serializers.ImageField()
    images = serializers.ListField(child=serializers.ImageField(), required=False)
    tags = serializers.ListField(child=serializers.IntegerField(), required=False)


class SellerMyInfoSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=20)
    profile_image = serializers.CharField(source='user.profile_image.url')
    item_count = serializers.IntegerField()
    temperature = serializers.FloatField()


class SellerInfoSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=20)
    profile_image = serializers.CharField(source='user.profile_image.url')
    item_count = serializers.IntegerField()
    temperature = serializers.FloatField()
