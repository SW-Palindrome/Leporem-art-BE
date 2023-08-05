from apps.chats.repositories import ChatRoomRepository, MessageRepository


class ChatRoomService:
    def create_by_buyer(self, buyer_id, seller_id, text, image):
        chat_room_repository = ChatRoomRepository()
        return chat_room_repository.create_by_buyer(buyer_id, seller_id, text, image)


class MessageService:
    def create(self, chat_room_uuid, user_id, text, image, message_uuid=None):
        message_repository = MessageRepository()
        return message_repository.create(chat_room_uuid, user_id, text, image, message_uuid)
