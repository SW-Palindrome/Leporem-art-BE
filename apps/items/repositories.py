from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Count, F, Subquery
from django.utils import timezone

from apps.items.models import Item, ItemImage, Like
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
        categories,
        colors,
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
        for category_id in categories:
            item.category_mappings.create(
                category_id=category_id,
            )
        for color_id in colors:
            item.color_mappings.create(
                color_id=color_id,
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

    def get_item(self, item_id) -> Item:
        return Item.objects.get(item_id=item_id)

    def filter_item(self):
        search_item = Item.objects.order_by('-display_dt').annotate(
            nickname=F('seller__user__nickname'),
            like_count=Count('likes'),
        )
        return search_item

    def item_detail(self, item_id, buyer_id):
        '''buyer가 item에 대한 좋아요 여부 판단하기 위한 Like model의 item_id와 buyer_id'''
        like_subquery = Like.objects.filter(item_id=item_id, buyer_id=buyer_id)
        detailed_item = Item.objects.annotate(
            nickname=F('seller__user__nickname'),
            category=F('category_mappings__category__category'),
            temperature=F('seller__temperature'),
            buyer_id=Subquery(like_subquery.values('buyer_id')[:1]),
        ).filter(item_id=item_id)
        return detailed_item
