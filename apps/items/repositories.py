from apps.items.models import Item
from apps.users.models import User


class ItemRepository:
    def load_nickname(self, nickname):
        try:
            nickname_info = User.objects.select_related('seller', 'items').get(nickname=nickname)
            return nickname_info
        except User.DoesNotExist:
            return None

    def load_image(self, image):
        try:
            image_info = Item.objects.select_related('item_images').filter(is_thumbnail=True, image=image)
            return image_info
        except Item.DoesNotExist:
            return None

    def load_like(self, item):
        try:
            like_count = Item.objects.select_related('likes').filter(item=item).count()
            return like_count
        except Item.DoesNotExist:
            return None

    def load_item_list(self, title, price):
        try:
            item_info = Item.objects.filter(title=title, price=price)
            return item_info
        except Item.DoesNotExist:
            return None
