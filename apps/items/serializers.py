from rest_framework import serializers


class ItemListSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
    nickname = serializers.CharField()
    title = serializers.CharField()
    price = serializers.IntegerField()
    thumbnail_image = serializers.CharField(source='thumbnail_image.image.url')
    likes = serializers.IntegerField(source='like_count')
    avg_rating = serializers.DecimalField(max_digits=2, decimal_places=1)
    time_diff = serializers.DurationField()
    is_liked = serializers.BooleanField()

    class Meta:
        fields = ('item_id', 'nickname', 'title', 'price', 'thumbnail_image', 'likes', 'avg_rating', 'time_diff')


def get_images(item):
    images = item.item_images.filter(is_thumbnail=False)
    image_urls = [image.image.url for image in images]
    return image_urls


def get_category(item):
    categories = item.category_mappings.all()
    category_list = [category.category.category for category in categories]
    return category_list


class BuyerDetailedItemSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
    nickname = serializers.CharField()
    profile_image = serializers.CharField(source='seller.user.profile_image.url')
    title = serializers.CharField()
    description = serializers.CharField()
    price = serializers.IntegerField()
    temperature = serializers.FloatField()
    current_amount = serializers.IntegerField()
    shorts = serializers.CharField(source='shorts.url')
    thumbnail_image = serializers.CharField(source='thumbnail_image.image.url')
    images = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    like = serializers.SerializerMethodField()
    width = serializers.DecimalField(max_digits=6, decimal_places=2)
    depth = serializers.DecimalField(max_digits=6, decimal_places=2)
    height = serializers.DecimalField(max_digits=6, decimal_places=2)

    def get_images(self, obj):
        return get_images(obj)

    def get_category(self, obj):
        return get_category(obj)

    def get_like(self, obj):
        if obj.buyer_id:
            return True
        return False


class ReviewSerializer(serializers.Serializer):
    comment = serializers.CharField()
    rating = serializers.DecimalField(max_digits=2, decimal_places=1)
    writer = serializers.CharField()
    write_dt = serializers.DateTimeField()

    class Meta:
        fields = ('comment', 'rating', 'writer', 'write_dt')
