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
