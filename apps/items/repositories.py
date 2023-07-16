from urllib.parse import urljoin
from django.db.models import Count
from apps.items.models import Item, ItemImage, Like


class ItemRepository:
    def load_nickname(self):
        try:
            nickname_info = (
                Item.objects.select_related('seller', 'seller__user')
                .filter(seller__items__isnull=False)
                .order_by('-display_dt')
                .values_list('seller__user__nickname')
            )
            return nickname_info
        except Item.DoesNotExist:
            return None

    def load_item_list(self):
        try:
            item_info = Item.objects.filter(seller__items__isnull=False).order_by('-display_dt').values_list('title', 'price')
            return item_info
        except Item.DoesNotExist:
            return None

    def load_image(self):
        try:
            image_info = ItemImage.objects.select_related('item').order_by('-item__display_dt').filter(is_thumbnail=True)
            image_url = [
                urljoin('https://leporem-art-media-dev.s3.ap-northeast-2.amazonaws.com/items/item_image/', str(image))
                for image in image_info
            ]
            return image_url
        except ItemImage.DoesNotExist:
            return None

    def load_like(self):
        try:
            likes = Like.objects.select_related('item').values('item').order_by('-item__display_dt').annotate(like_count=Count('item')).values('like_count')
            return likes
        except likes.DoesNotExist:
            return None
