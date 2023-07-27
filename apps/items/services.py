from apps.items.repositories import ItemRepository


class ItemService:
    def filter_items(self):
        item_repository = ItemRepository()
        return item_repository.filter_item()

    def buyer_detailed_item(self, item_id, buyer_id):
        item_repository = ItemRepository()
        detailed_item = item_repository.item_detail(item_id, buyer_id)
        if not detailed_item:
            return None
        return detailed_item


class LikeService:
    def check_like(self, item_id, buyer_id):
        item_repository = ItemRepository()
        if item_repository.get_like(item_id, buyer_id):
            return True
        return False

    def on_like(self, item_id, buyer_id):
        item_repository = ItemRepository()
        if not self.check_like(item_id, buyer_id):
            item_repository.post_like(item_id, buyer_id)
            return True
        return False

    def off_like(self, item_id, buyer_id):
        item_repository = ItemRepository()
        if self.check_like(item_id, buyer_id):
            item_repository.delete_like(item_id, buyer_id)
            return True
        return False
