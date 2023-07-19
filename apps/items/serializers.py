from rest_framework import serializers


def get_thumbnail_image(item):
    return item.item_images.get(is_thumbnail=True).image.url


class ItemListSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
    nickname = serializers.CharField()
    title = serializers.CharField()
    price = serializers.IntegerField()
    thumbnail_image = serializers.SerializerMethodField()
    likes = serializers.IntegerField(source='like_count')

    def get_thumbnail_image(self, obj):
        return get_thumbnail_image(obj)

    class Meta:
        fields = ('item_id', 'nickname', 'title', 'price', 'thumbnail_image', 'likes')
