from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Count, F
from django.utils import timezone

from apps.items.models import Item, ItemImage
from apps.sellers.models import Seller


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

        return item

    def load_item_list(self):
        item_info = Item.objects.order_by('-display_dt').annotate(
            like_count=Count('likes'), nickname=F('seller__user__nickname')
        )
        return item_info

    def get_item(self, item_id) -> Item:
        return Item.objects.get(item_id=item_id)
