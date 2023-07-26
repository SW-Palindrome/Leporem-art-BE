from rest_framework import serializers


class ItemListSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
    nickname = serializers.CharField()
    title = serializers.CharField()
    price = serializers.IntegerField()
    thumbnail_image = serializers.CharField(source='thumbnail_image.image.url')
    likes = serializers.IntegerField(source='like_count')

    class Meta:
        fields = ('item_id', 'nickname', 'title', 'price', 'thumbnail_image', 'likes')


def get_images(item):
    images = item.item_images.filter(is_thumbnail=False)
    image_urls = [image.image.url for image in images]
    return image_urls


class BuyerDetailedItemSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
    buyer_id = serializers.CharField()
    nickname = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    price = serializers.IntegerField()
    temperature = serializers.FloatField()
    current_amount = serializers.IntegerField()
    shorts = serializers.CharField(source='shorts.url')
    thumbnail_image = serializers.CharField(source='thumbnail_image.image.url')
    images = serializers.SerializerMethodField()
    category = serializers.CharField()
    like = serializers.SerializerMethodField()
    width = serializers.DecimalField(max_digits=6, decimal_places=2)
    depth = serializers.DecimalField(max_digits=6, decimal_places=2)
    height = serializers.DecimalField(max_digits=6, decimal_places=2)

    def get_images(self, obj):
        return get_images(obj)

    def get_like(self, obj):
        if obj.buyer_id:
            return True
        return False
