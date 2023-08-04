from django.db.models import F, Max, Prefetch

from apps.chats.models import ChatRoom, Message


class ChatRoomRepository:
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
