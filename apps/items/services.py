from apps.items.repositories import ItemRepository, LikeRepository


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
