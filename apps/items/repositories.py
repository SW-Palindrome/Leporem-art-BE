from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Avg, Count, Exists, F, OuterRef, Subquery
from django.db.models.functions import Round
from django.utils import timezone

from apps.buyers.models import Buyer
from apps.items.exceptions import CurrentAmountException
from apps.items.models import Item, ItemImage, Like, RecentlyViewedItem
from apps.orders.models import Review
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
        shorts_url,
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
            shorts=shorts_url,
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
        current_amount,
        title,
        description,
        shorts_url,
        width,
        depth,
        height,
        thumbnail_image,
        images,
        categories,
        colors,
    ):
        try:
            item = Seller.objects.get(seller_id=seller_id).items.get(item_id=item_id)
        except Item.DoesNotExist:
            raise PermissionDenied

        item.price = price
        item.title = title
        item.description = description
        item.shorts = shorts_url
        item.width = width
        item.depth = depth
        item.height = height
        amount_diff = current_amount - item.current_amount
        item.max_amount = item.max_amount + amount_diff
        item.current_amount = current_amount
        item.save()

        item.item_images.all().delete()
        item.category_mappings.all().delete()
        item.color_mappings.all().delete()

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

    def get_item(self, item_id) -> Item:
        return Item.objects.get(item_id=item_id)

    def get_items(self, buyer_id):
        search_item = (
            Item.objects.order_by('-display_dt')
            .filter(
                seller__user__inactive_datetime__isnull=True,
                deleted_date__isnull=True,
            )
            .annotate(
                nickname=F('seller__user__nickname'),
                like_count=Count('likes', distinct=True),
                avg_rating=Round(Avg('orders__review__rating'), 1),
                time_diff=timezone.now() - F('display_dt'),
                is_liked=Exists(Like.objects.filter(item=OuterRef('item_id'), buyer_id=buyer_id)),
            )
        )
        return search_item

    def item_detail(self, item_id, buyer_id):
        '''buyer가 item에 대한 좋아요 여부 판단하기 위한 Like model의 item_id와 buyer_id'''
        like_subquery = Like.objects.filter(item_id=item_id, buyer_id=buyer_id)
        detailed_item = Item.objects.annotate(
            nickname=F('seller__user__nickname'),
            temperature=F('seller__temperature'),
            buyer_id=Subquery(like_subquery.values('buyer_id')[:1]),
        ).get(item_id=item_id)
        return detailed_item

    def seller_item_detail(self, item_id, seller_id):
        detailed_item = Item.objects.annotate(
            nickname=F('seller__user__nickname'),
            temperature=F('seller__temperature'),
        ).get(item_id=item_id, seller=seller_id)
        return detailed_item

    def detailed_item_review(self, item_id, seller_id):
        reviews = (
            Review.objects.annotate(
                item_id=F('order__item__item_id'),
                seller_id=F('order__item__seller'),
                writer=F('order__buyer__user__nickname'),
                write_dt=F('modified'),
            )
            .filter(item_id=item_id, seller_id=seller_id)
            .order_by('-write_dt')
        )
        return reviews

    def get_favorite_items(self, buyer):
        liked_dates = Subquery(Like.objects.filter(item=OuterRef('item_id'), buyer=buyer).values('created')[:1])
        favorite_items = (
            Item.objects.annotate(
                nickname=F('seller__user__nickname'),
                is_liked=Exists(Like.objects.filter(item=OuterRef('item_id'), buyer=buyer)),
                liked_dates=liked_dates,
            )
            .order_by('-liked_dates')
            .filter(is_liked=True, deleted_date__isnull=True)
        )
        return favorite_items

    def change_current_amount(self, item_id, seller_id, action):
        try:
            item = Seller.objects.get(seller_id=seller_id).items.get(item_id=item_id)
        except Item.DoesNotExist:
            raise PermissionDenied

        action = int(action)

        if action == 1:
            item.current_amount += 1
            if item.current_amount > 99:
                raise CurrentAmountException("The quantity of the item exceeds the limit.")
        else:
            item.current_amount -= 1
            if item.current_amount < 0:
                raise CurrentAmountException("The quantity of the item is less than 1.")
        item.save()

    def get_guest_items(self):
        search_item = (
            Item.objects.filter(
                seller__user__inactive_datetime__isnull=True,
                deleted_date__isnull=True,
            )
            .order_by('-display_dt')
            .annotate(
                nickname=F('seller__user__nickname'),
                like_count=Count('likes', distinct=True),
                avg_rating=Round(Avg('orders__review__rating'), 1),
                time_diff=timezone.now() - F('display_dt'),
                is_liked=Exists(Like.objects.filter(item=OuterRef('item_id'), buyer_id=None)),
            )
        )
        return search_item

    def get_guest_detailed_item(self, item_id):
        like_subquery = Like.objects.filter(item_id=item_id, buyer_id=None)
        detailed_item = Item.objects.annotate(
            nickname=F('seller__user__nickname'),
            temperature=F('seller__temperature'),
            buyer_id=Subquery(like_subquery.values('buyer_id')[:1]),
        ).get(item_id=item_id)
        return detailed_item

    @transaction.atomic
    def delete(self, seller_id, item_id):
        try:
            item = Seller.objects.get(seller_id=seller_id).items.get(item_id=item_id)
        except Item.DoesNotExist:
            raise PermissionDenied

        item.deleted_date = timezone.now()
        item.save()
        return item


class LikeRepository:
    def get_like(self, item_id, buyer_id):
        is_liked = Like.objects.filter(item_id=item_id, buyer_id=buyer_id)
        return is_liked

    def post_like(self, item_id, buyer_id):
        Like.objects.create(item_id=item_id, buyer_id=buyer_id)

    def delete_like(self, item_id, buyer_id):
        Like.objects.filter(item_id=item_id, buyer_id=buyer_id).delete()


class ViewedItemRepository:
    def post_viewed_item(self, item, buyer):
        buyer = Buyer.objects.get(pk=buyer)
        item = Item.objects.get(pk=item)
        RecentlyViewedItem.objects.create(item=item, buyer=buyer)

    def delete_viewed_item(self, item, buyer):
        viewed_item = RecentlyViewedItem.objects.filter(item=item, buyer=buyer)
        viewed_item.update(deleted_date=timezone.now())

    def get_viewed_items(self, buyer):
        recently_viewed_subquery = (
            RecentlyViewedItem.objects.filter(buyer=OuterRef('buyer'), item=OuterRef('item'), deleted_date__isnull=True)
            .order_by('-viewed_date')
            .values('viewed_date')[:1]
        )

        viewed_items = (
            RecentlyViewedItem.objects.annotate(
                nickname=F('item__seller__user__nickname'),
                title=F('item__title'),
                price=F('item__price'),
                is_liked=Exists(Like.objects.filter(item=OuterRef('item_id'), buyer=buyer)),
            )
            .filter(
                buyer=buyer,
                deleted_date__isnull=True,
                viewed_date=Subquery(recently_viewed_subquery),
                item__deleted_date__isnull=True,
            )
            .order_by('-viewed_date')
        )[:50]
        return viewed_items
