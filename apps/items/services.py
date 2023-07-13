from apps.items.repositories import ItemRepository

class LoadItemListService:
    def load_nickname(self, nickname):
        item_repository = ItemRepository()
        if not item_repository.load_nickname(nickname):
            return False
        return item_repository.load_nickname(nickname)

    def load_item(self, title, price):
        item_repository = ItemRepository()
        if not item_repository.load_item_list(title, price):
            return False
        return item_repository.load_item_list(title, price)

    def load_image(self, image):
        item_repository = ItemRepository()
        if not item_repository.load_image(image):
            return False
        return item_repository.load_image(image)

    def load_likes(self, item):
        item_repository = ItemRepository()
        if not item_repository.load_like(item):
            return False
        return item_repository.load_like(item)