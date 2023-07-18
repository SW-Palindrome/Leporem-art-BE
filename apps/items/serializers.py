from rest_framework import serializers


def get_nickname(item):
    return item.seller.user.nickname


def get_thumbnail_image(item):
    return item.item_images.get(is_thumbnail=True).image.url


def get_likes(item):
    return item.likes.count()


class ItemListSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
    nickname = serializers.SerializerMethodField()
    title = serializers.CharField()
    price = serializers.IntegerField()
    thumbnail_image = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    def get_nickname(self, obj):
        return get_nickname(obj)

    def get_thumbnail_image(self, obj):
        return get_thumbnail_image(obj)

    def get_likes(self, obj):
        return get_likes(obj)

    class Meta:
        fields = ('item_id', 'nickname', 'title', 'price', 'thumbnail_image', 'likes')
