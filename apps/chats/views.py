from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.chats.repositories import ChatRoomRepository
from apps.chats.serializers import (
    BuyerChatRoomCreateSerializer,
    BuyerChatRoomListSerializer,
    MessageCreateSerializer,
    SellerChatRoomListSerializer,
)
from apps.chats.services import ChatRoomService, MessageService
from apps.users.permissions import IsSeller


class BuyerChatRoomView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [FormParser, MultiPartParser]

    def get(self, request):
        chat_rooms = ChatRoomRepository().get_chat_rooms_by_buyer_id(request.user.buyer.buyer_id)
        serializer = BuyerChatRoomListSerializer(chat_rooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BuyerChatRoomCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            chat_room = ChatRoomService().create_by_buyer(
                buyer_id=request.user.buyer.buyer_id,
                seller_id=serializer.validated_data['seller_id'],
                text=serializer.validated_data.get('text'),
                image=serializer.validated_data.get('image'),
                chat_room_uuid=serializer.validated_data.get('chat_room_uuid'),
                message_uuid=serializer.validated_data.get('message_uuid'),
            )
        except ValueError as e:
            return Response({'message': str(e)}, status=400)
        return Response({'chat_room_id': chat_room.chat_room_id}, status=201)


class SellerChatRoomListView(APIView):
    permission_classes = [IsSeller]
    serializer_class = SellerChatRoomListSerializer

    def get(self, request):
        chat_rooms = ChatRoomRepository().get_chat_rooms_by_seller_id(request.user.seller.seller_id)
        serializer = self.serializer_class(chat_rooms, many=True)
        return Response(serializer.data)


class MessageCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageCreateSerializer
    parser_classes = [FormParser, MultiPartParser]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            message = MessageService().create(
                chat_room_uuid=serializer.validated_data['chat_room_uuid'],
                user_id=request.user.user_id,
                message_type=serializer.validated_data['type'],
                message=serializer.validated_data.get('text') or serializer.validated_data.get('image'),
                message_uuid=serializer.validated_data.get('message_uuid'),
            )
        except ValueError as e:
            return Response({'message': str(e)}, status=400)
        return Response({'message_id': message.message_id}, status=201)
