from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.utils import timezone

from apps.items.models import Item, ItemImage, ItemTagMapping
from apps.sellers.models import Seller


class ItemRepository:
    @transaction.atomic
    def register(
        self, seller_id, price, max_amount, title, description, shorts, width, depth, height, thumbnail_image, images, tags
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
        self, seller_id, item_id, price, max_amount, title, description, shorts, width, depth, height, thumbnail_image, images, tags
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
