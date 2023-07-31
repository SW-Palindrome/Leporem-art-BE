from apps.chats.repositories import MessageRepository


class MessageService:
    def create(self, chat_room_id, user_id, text, image):
        message_repository = MessageRepository()
        return message_repository.create(chat_room_id, user_id, text, image)
