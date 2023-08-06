from apps.chats.models import Message
from apps.chats.repositories import ChatRoomRepository, MessageRepository


class ChatRoomService:
    def create_by_buyer(self, buyer_id, seller_id, text, image, chat_room_uuid=None, message_uuid=None):
        chat_room_repository = ChatRoomRepository()
        return chat_room_repository.create_by_buyer(buyer_id, seller_id, text, image, chat_room_uuid, message_uuid)


class MessageService:
    def create(self, chat_room_uuid, user_id, message_type, message, message_uuid=None):
        message_repository = MessageRepository()
        match message_type:
            case Message.Type.TEXT:
                return message_repository.create_text(
                    chat_room_uuid=chat_room_uuid,
                    user_id=user_id,
                    text=message,
                    message_uuid=message_uuid,
                )
            case Message.Type.IMAGE:
                return message_repository.create_image(
                    chat_room_uuid=chat_room_uuid,
                    user_id=user_id,
                    image=message,
                    message_uuid=message_uuid,
                )
            case Message.Type.ITEM_SHARE:
                return message_repository.create_item_share(
                    chat_room_uuid=chat_room_uuid,
                    user_id=user_id,
                    item_id=message,
                    message_uuid=message_uuid,
                )
            case Message.Type.ITEM_INQUIRY:
                return message_repository.create_item_inquiry(
                    chat_room_uuid=chat_room_uuid,
                    user_id=user_id,
                    item_id=message,
                    message_uuid=message_uuid,
                )
            case Message.Type.ORDER:
                return message_repository.create_order(
                    chat_room_uuid=chat_room_uuid,
                    user_id=user_id,
                    order_id=message,
                    message_uuid=message_uuid,
                )
