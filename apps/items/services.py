from apps.buyers.models import Buyer
from apps.buyers.respositories import BuyerRepository
from apps.items.exceptions import BuyerDoesNotExist, ItemDoesNotExist
from apps.items.models import Item
from apps.items.repositories import ItemRepository, LikeRepository, ViewedItemRepository


class ItemService:
    def filter_items(self, buyer_id):
        item_repository = ItemRepository()
        return item_repository.get_items(buyer_id=buyer_id)

    def buyer_detailed_item(self, item_id, buyer_id):
        item_repository = ItemRepository()
        detailed_item = item_repository.item_detail(item_id, buyer_id)
        if not detailed_item:
            return None
        return detailed_item

    def seller_detailed_item(self, item_id, seller_id):
        item_repository = ItemRepository()
        detailed_item = item_repository.seller_item_detail(item_id, seller_id)
        if not detailed_item:
            return None
        return detailed_item

    def detailed_item_review(self, item_id):
        item_repository = ItemRepository()
        reviews = item_repository.detailed_item_review(item_id)
        if not reviews:
            return None
        return reviews

    def favorite_items(self, buyer):
        item_repository = ItemRepository()
        try:
            BuyerRepository().get_buyer(buyer)
            favorite_items = item_repository.get_favorite_items(buyer)
            return favorite_items
        except Buyer.DoesNotExist:
            raise BuyerDoesNotExist("Buyer does not exist.")

    def guest_items(self):
        items = ItemRepository().get_guest_items()
        return items

    def guest_detailed_item(self, item_id):
        detailed_item = ItemRepository().get_guest_detailed_item(item_id)
        return detailed_item


class LikeService:
    def check_like(self, item_id, buyer_id):
        like_repository = LikeRepository()
        if like_repository.get_like(item_id, buyer_id):
            return True
        return False

    def on_like(self, item_id, buyer_id):
        like_repository = LikeRepository()
        if not self.check_like(item_id, buyer_id):
            like_repository.post_like(item_id, buyer_id)
            return True
        return False

    def off_like(self, item_id, buyer_id):
        like_repository = LikeRepository()
        if self.check_like(item_id, buyer_id):
            like_repository.delete_like(item_id, buyer_id)
            return True
        return False


class ViewedItemService:
    def add_viewed_item(self, item_id, buyer_id):
        viewed_item_repository = ViewedItemRepository()
        try:
            ItemRepository().get_item(item_id)
            try:
                BuyerRepository().get_buyer(buyer_id)
                viewed_item_repository.post_viewed_item(item_id, buyer_id)
            except Buyer.DoesNotExist:
                raise BuyerDoesNotExist("Buyer does not exist.")
        except Item.DoesNotExist:
            raise ItemDoesNotExist("Item does not exist.")

    def delete_viewed_item(self, item_id, buyer_id):
        viewed_item_repository = ViewedItemRepository()
        try:
            ItemRepository().get_item(item_id)
            try:
                BuyerRepository().get_buyer(buyer_id)
                viewed_item_repository.delete_viewed_item(item_id, buyer_id)
            except Buyer.DoesNotExist:
                raise BuyerDoesNotExist("Buyer does not exist.")
        except Item.DoesNotExist:
            raise ItemDoesNotExist("Item does not exist.")

    def viewed_items(self, buyer_id):
        viewed_item_repository = ViewedItemRepository()
        try:
            BuyerRepository().get_buyer(buyer_id)
            viewed_items = viewed_item_repository.get_viewed_items(buyer_id)
            if viewed_items:
                return viewed_items
            raise ItemDoesNotExist("Item does not exist.")
        except Buyer.DoesNotExist:
            raise BuyerDoesNotExist("Buyer does not exist.")
