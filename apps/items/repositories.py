from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.utils import timezone

from apps.items.models import Item, ItemImage, ItemTagMapping
from apps.sellers.models import Seller
from urllib.parse import urljoin
from django.db.models import Count

class ItemRepository:
    @transaction.atomic
    def register(
        self,
        seller_id,
        price,
        max_amount,
        title,
        description,
        shorts,
        width,
        depth,
        height,
        thumbnail_image,
        images,
        tags,
    ):
        seller = Seller.objects.get(seller_id=seller_id)
        item = Item.objects.create(
            seller=seller,
            price=price,
            max_amount=max_amount,
            current_amount=max_amount,
            title=title,
            description=description,
            shorts=shorts,
            width=width,
            depth=depth,
            height=height,
            display_dt=timezone.now(),
        )
        ItemImage.objects.create(
            item=item,
            image=thumbnail_image,
            is_thumbnail=True,
        )
        for image in images:
            ItemImage.objects.create(
                item=item,
                image=image,
            )
        for tag in tags:
            ItemTagMapping.objects.create(
                item=item,
                tag=tag,
            )
        return item

    @transaction.atomic
    def modify(
        self,
        seller_id,
        item_id,
        price,
        max_amount,
        title,
        description,
        shorts,
        width,
        depth,
        height,
        thumbnail_image,
        images,
        tags,
    ):
        try:
            item = Seller.objects.get(seller_id=seller_id).items.get(item_id=item_id)
        except Item.DoesNotExist:
            raise PermissionDenied

        item.price = price
        item.max_amount = max_amount
        item.title = title
        item.description = description
        item.shorts = shorts
        item.width = width
        item.depth = depth
        item.height = height
        item.thumbnail_image = thumbnail_image
        item.save()

        item.item_images.all().delete()
        item.item_tag_mappings.all().delete()

        for image in images:
            ItemImage.objects.create(
                item=item,
                image=image,
            )
        for tag in tags:
            ItemTagMapping.objects.create(
                item=item,
                tag=tag,
            )

        return item

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
            item_info = (
                Item.objects.filter(seller__items__isnull=False).order_by('-display_dt').values_list('title', 'price')
            )
            return item_info
        except Item.DoesNotExist:
            return None

    def load_image(self):
        try:
            image_info = (
                ItemImage.objects.select_related('item').order_by('-item__display_dt').filter(is_thumbnail=True)
            )
            image_url = [
                urljoin('https://leporem-art-media-dev.s3.ap-northeast-2.amazonaws.com/items/item_image/', str(image))
                for image in image_info
            ]
            return image_url
        except ItemImage.DoesNotExist:
            return None

    def load_like(self):
        try:
            likes = (
                Like.objects.select_related('item')
                .values('item')
                .order_by('-item__display_dt')
                .annotate(like_count=Count('item'))
                .values('like_count')
            )
            return likes
        except likes.DoesNotExist:
            return None
