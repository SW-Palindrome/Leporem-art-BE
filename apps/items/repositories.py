from django.db.models import Count, F

from apps.items.models import Item


class ItemRepository:
    def load_item_list(self):
        item_info = Item.objects.order_by('-display_dt').annotate(
            like_count=Count('likes'), nickname=F('seller__user__nickname')
        )
        return item_info
