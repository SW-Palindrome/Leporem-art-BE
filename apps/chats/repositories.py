import uuid

from django.db import transaction
from django.db.models import F, Max, Prefetch

from apps.buyers.models import Buyer
from apps.chats.models import ChatRoom, Message
from apps.items.models import Item
from apps.orders.models import Order


class ChatRoomRepository:
    @transaction.atomic
    def create_by_buyer(self, buyer_id, seller_id, text, image, chat_room_uuid=None, message_uuid=None):
        """판매자가 채팅방을 생성합니다."""
        if bool(text) == bool(image):
            raise ValueError('text와 image 중 하나만 입력해주세요.')

        chat_room = ChatRoom.objects.create(buyer_id=buyer_id, seller_id=seller_id, uuid=chat_room_uuid or uuid.uuid4())
        buyer = Buyer.objects.get(buyer_id=buyer_id)
        MessageRepository().create(chat_room.uuid, buyer.user_id, text, image, message_uuid)
        return chat_room

    def get_chat_rooms_by_buyer_id(self, buyer_id):
        return (
            ChatRoom.objects.filter(buyer_id=buyer_id)
            .select_related('seller__user')
            .prefetch_related(Prefetch('messages', queryset=Message.objects.order_by('write_datetime')))
            .annotate(
                max_write_datetime=Max('messages__write_datetime'),
                opponent_nickname=F('seller__user__nickname'),
                opponent_user_id=F('seller__user_id'),
            )
            .order_by('-max_write_datetime')
        )

    def get_chat_rooms_by_seller_id(self, seller_id):
        return (
            ChatRoom.objects.filter(seller_id=seller_id)
            .select_related('buyer__user')
            .prefetch_related(Prefetch('messages', queryset=Message.objects.order_by('write_datetime')))
            .annotate(
                max_write_datetime=Max('messages__write_datetime'),
                opponent_nickname=F('buyer__user__nickname'),
                opponent_user_id=F('buyer__user_id'),
            )
            .order_by('-max_write_datetime')
        )


class MessageRepository:
    def _validate_user_in_chat_room(self, chat_room, user_id):
        if user_id not in [chat_room.buyer.user_id, chat_room.seller.user_id]:
            raise ValueError('채팅방에 참여하지 않은 유저입니다.')

    def _validate_item(self, item_id):
        if not Item.objects.filter(item_id=item_id).exists():
            raise ValueError('존재하지 않는 아이템입니다.')

    def create_text(self, chat_room_uuid, user_id, text, message_uuid=None):
        chat_room = ChatRoom.objects.get(uuid=chat_room_uuid)
        self._validate_user_in_chat_room(chat_room, user_id)

        return Message.objects.create(
            chat_room=chat_room,
            user_id=user_id,
            text=text,
            uuid=message_uuid or uuid.uuid4(),
            type=Message.Type.TEXT,
        )

    def create_image(self, chat_room_uuid, user_id, image, message_uuid=None):
        chat_room = ChatRoom.objects.get(uuid=chat_room_uuid)
        self._validate_user_in_chat_room(chat_room, user_id)

        return Message.objects.create(
            chat_room=chat_room,
            user_id=user_id,
            text='',
            image=image,
            uuid=message_uuid or uuid.uuid4(),
            type=Message.Type.IMAGE,
        )

    def create_item_share(self, chat_room_uuid, user_id, item_id, message_uuid=None):
        chat_room = ChatRoom.objects.get(uuid=chat_room_uuid)
        self._validate_user_in_chat_room(chat_room, user_id)
        self._validate_item(item_id)

        return Message.objects.create(
            chat_room=chat_room,
            user_id=user_id,
            text=str(item_id),
            uuid=message_uuid or uuid.uuid4(),
            type=Message.Type.ITEM_SHARE,
        )

    def create_item_inquiry(self, chat_room_uuid, user_id, item_id, message_uuid=None):
        chat_room = ChatRoom.objects.get(uuid=chat_room_uuid)
        self._validate_user_in_chat_room(chat_room, user_id)
        self._validate_item(item_id)

        return Message.objects.create(
            chat_room=chat_room,
            user_id=user_id,
            text=str(item_id),
            uuid=message_uuid or uuid.uuid4(),
            type=Message.Type.ITEM_INQUIRY,
        )

    def create_order(self, chat_room_uuid, user_id, order_id, message_uuid=None):
        chat_room = ChatRoom.objects.get(uuid=chat_room_uuid)
        self._validate_user_in_chat_room(chat_room, user_id)
        if not Order.objects.filter(order_id=order_id).exists():
            raise ValueError('존재하지 않는 아이템입니다.')

        return Message.objects.create(
            chat_room=chat_room,
            user_id=user_id,
            text=str(order_id),
            uuid=message_uuid or uuid.uuid4(),
            type=Message.Type.ORDER,
        )
