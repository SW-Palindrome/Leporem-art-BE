from django.db.models import F, Max, OuterRef, Subquery

from apps.chats.models import ChatRoom, Message


class ChatRoomRepository:
    def get_chat_rooms_by_buyer_id(self, buyer_id):
        last_message = Subquery(
            Message.objects.filter(chat_room_id=OuterRef('chat_room_id')).order_by('-write_datetime').values('text')[:1]
        )
        return (
            ChatRoom.objects.filter(buyer_id=buyer_id)
            .annotate(
                last_message_datetime=Max('messages__write_datetime'),
                last_message=last_message,
                opponent_nickname=F('seller__user__nickname'),
            )
            .select_related('seller__user')
        )


class MessageRepository:
    def create(self, chat_room_id, user_id, text, image):
        if bool(text) == bool(image):
            raise ValueError('text와 image 중 하나만 입력해주세요.')

        chat_room = ChatRoom.objects.get(chat_room_id=chat_room_id)
        if user_id not in [chat_room.buyer.user_id, chat_room.seller.user_id]:
            raise ValueError('채팅방에 참여하지 않은 유저입니다.')

        return Message.objects.create(
            chat_room_id=chat_room_id,
            user_id=user_id,
            text=text,
            image=image,
        )
