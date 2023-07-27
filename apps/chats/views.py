from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.chats.repositories import ChatRoomRepository
from apps.chats.serializers import BuyerChatRoomListSerializer


class BuyerChatRoomListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BuyerChatRoomListSerializer

    def get(self, request):
        chat_rooms = ChatRoomRepository().get_chat_rooms_by_buyer_id(request.user.buyer.buyer_id)
        serializer = self.serializer_class(chat_rooms, many=True)
        return Response(serializer.data)
