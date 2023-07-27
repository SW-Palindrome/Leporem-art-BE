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
