from apps.items.repositories import ItemRepository


class LoadItemListService:
    def load_nickname(self):
        item_repository = ItemRepository()
        if not item_repository.load_nickname():
            return False
        return item_repository.load_nickname()

    def load_item(self):
        item_repository = ItemRepository()
        if not item_repository.load_item_list():
            return False
        return item_repository.load_item_list()

    def load_image(self):
        item_repository = ItemRepository()
        if not item_repository.load_image():
            return False
        return item_repository.load_image()

    def load_likes(self):
        item_repository = ItemRepository()
        if not item_repository.load_like():
            return False
        return item_repository.load_like()
