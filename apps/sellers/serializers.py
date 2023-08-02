from rest_framework import serializers


class SellerRegisterSerializer(serializers.Serializer):
    email = serializers.RegexField(r'^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9-]+\.)+ac\.kr$')


class SellerVerifySerializer(serializers.Serializer):
    verify_code = serializers.CharField(max_length=6)


class SellerItemSerializer(serializers.Serializer):
    price = serializers.IntegerField()
    amount = serializers.IntegerField()
    title = serializers.CharField(max_length=46)
    description = serializers.CharField(max_length=255)
    shorts = serializers.FileField()
    width = serializers.DecimalField(max_digits=6, decimal_places=2, required=False)
    depth = serializers.DecimalField(max_digits=6, decimal_places=2, required=False)
    height = serializers.DecimalField(max_digits=6, decimal_places=2, required=False)
    thumbnail_image = serializers.ImageField()
    images = serializers.ListField(child=serializers.ImageField(), required=False)
    categories = serializers.ListField(child=serializers.IntegerField(), required=False)
    colors = serializers.ListField(child=serializers.IntegerField(), required=False)


class SellerMyInfoSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=20)
    profile_image = serializers.CharField(source='user.profile_image.url')
    total_transactions = serializers.IntegerField()
    retention_rate = serializers.FloatField()
    item_count = serializers.IntegerField()
    temperature = serializers.FloatField()
    description = serializers.CharField(max_length=80)


class SellerInfoSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=20)
    profile_image = serializers.CharField(source='user.profile_image.url')
    item_count = serializers.IntegerField()
    temperature = serializers.FloatField()
    description = serializers.CharField(max_length=80)


class DescriptionSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=255)


class SellerMyOrderSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    item_id = serializers.IntegerField()
    item_title = serializers.CharField(source='item.title')
    item_thumbnail_image = serializers.CharField(source='item.thumbnail_image.image.url')
    price = serializers.IntegerField()
    ordered_datetime = serializers.DateTimeField()
    order_status = serializers.CharField(source='get_order_status_display')
    buyer = serializers.CharField(source='buyer.user.nickname')


class TransactionSerializer(serializers.Serializer):
    total_transactions = serializers.IntegerField()
    total_rate = serializers.FloatField()
