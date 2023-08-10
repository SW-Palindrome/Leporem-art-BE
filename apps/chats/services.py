import uuid

from django.db import transaction

from apps.buyers.respositories import BuyerRepository
from apps.chats.models import Message
from apps.chats.repositories import ChatRoomRepository, MessageRepository


class ChatRoomService:
    @transaction.atomic
    def create_by_buyer(self, buyer_id, seller_id, text, image, message_type, chat_room_uuid=None, message_uuid=None):
        chat_room_repository = ChatRoomRepository()
        message_service = MessageService()
        chat_room = chat_room_repository.create_by_buyer(buyer_id, seller_id, chat_room_uuid)
        message_service.create(
            chat_room_uuid=chat_room_uuid,
            user_id=BuyerRepository().get_buyer(buyer_id=buyer_id).user_id,
            message_type=message_type,
            message=text or image,
            message_uuid=message_uuid,
        )
        return chat_room


class MessageService:
    def create(self, chat_room_uuid, user_id, message_type, message, message_uuid=None):
        message_repository = MessageRepository()
        message_uuid = message_uuid or uuid.uuid4()
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
