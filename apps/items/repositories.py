from django.db import transaction
from django.utils import timezone

from apps.items.models import Item, ItemImage, ItemTagMapping


class ItemRepository:
    @transaction.atomic
    def register(
        self, seller, price, max_amount, title, description, shorts, width, depth, height, thumbnail_image, images, tags
    ):
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
