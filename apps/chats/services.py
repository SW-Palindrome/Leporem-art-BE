import uuid

from django.db import transaction

from apps.buyers.respositories import BuyerRepository
from apps.chats.models import Message
from apps.chats.repositories import ChatRoomRepository, MessageRepository
from apps.notifications.services import NotificationService
from apps.users.models import User
from utils.files import create_presigned_url


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
                message = message_repository.create_text(
                    chat_room_uuid=chat_room_uuid,
                    user_id=user_id,
                    text=message,
                    message_uuid=message_uuid,
                )
            case Message.Type.IMAGE:
                message = message_repository.create_image(
                    chat_room_uuid=chat_room_uuid,
                    user_id=user_id,
                    image=message,
                    message_uuid=message_uuid,
                )
            case Message.Type.ITEM_SHARE:
                message = message_repository.create_item_share(
                    chat_room_uuid=chat_room_uuid,
                    user_id=user_id,
                    item_id=message,
                    message_uuid=message_uuid,
                )
            case Message.Type.ITEM_INQUIRY:
                message = message_repository.create_item_inquiry(
                    chat_room_uuid=chat_room_uuid,
                    user_id=user_id,
                    item_id=message,
                    message_uuid=message_uuid,
                )
            case Message.Type.ORDER:
                message = message_repository.create_order(
                    chat_room_uuid=chat_room_uuid,
                    user_id=user_id,
                    order_id=message,
                    message_uuid=message_uuid,
                )
            case _:
                message = message_repository.create_text(
                    chat_room_uuid=chat_room_uuid,
                    user_id=user_id,
                    text=message,
                    message_uuid=message_uuid,
                )
        self._send_notification(message=message)
        return message

    def read(self, user_id, chat_room_uuid, message_uuid):
        chat_room = MessageRepository().get_chat_room_by_message_uuid(message_uuid)
        if chat_room.uuid != chat_room_uuid or user_id not in [chat_room.buyer.user_id, chat_room.seller.user_id]:
            raise ValueError('채팅방에 참여하지 않은 유저입니다.')
        if chat_room.buyer.user_id == chat_room.seller.user_id:
            return MessageRepository().read_my_message(
                user_id=user_id,
                chat_room_uuid=chat_room_uuid,
                message_uuid=message_uuid,
            )
        return MessageRepository().read(user_id=user_id, chat_room_uuid=chat_room_uuid, message_uuid=message_uuid)

    def _send_notification(self, message: Message):
        chat_room = message.chat_room
        sender: User = chat_room.buyer.user if message.user_id == chat_room.buyer.user_id else chat_room.seller.user
        receiver: User = chat_room.seller.user if message.user_id == chat_room.buyer.user_id else chat_room.buyer.user

        NotificationService().send(
            user=receiver,
            title=f'{sender.nickname}',
            body=message.message_display,
            deep_link=f'/chat/{chat_room.uuid}',
        )

    def get_presigned_url_to_post_image(self, extension='jpg'):
        return create_presigned_url(f'{Message.image.field.upload_to}{str(uuid.uuid4())}.{extension}')
