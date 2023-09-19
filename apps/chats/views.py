from rest_framework.generics import ListAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.chats.repositories import ChatRoomRepository, MessageRepository
from apps.chats.serializers import (
    BuyerChatRoomCreateSerializer,
    BuyerChatRoomListAllMessagesSerializer,
    BuyerChatRoomListSerializer,
    MessageCreateSerializer,
    MessageReadSerializer,
    MessageSerializer,
    SellerChatRoomListAllMessagesSerializer,
    SellerChatRoomListSerializer,
)
from apps.chats.services import ChatRoomService, MessageService
from apps.users.permissions import IsInChatRoom, IsSeller


class BuyerChatRoomView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [FormParser, MultiPartParser]

    def get(self, request):
        chat_rooms = ChatRoomRepository().get_chat_rooms_by_buyer_id(request.user.buyer.buyer_id)
        serializer = self._get_serializer_class()
        return Response(serializer(chat_rooms, many=True).data)

    def _get_serializer_class(self):
        if self.request.query_params.get('only_last_message'):
            return BuyerChatRoomListSerializer
        return BuyerChatRoomListAllMessagesSerializer

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
                message_type=serializer.validated_data.get('message_type'),
            )
        except ValueError as e:
            return Response({'message': str(e)}, status=400)
        return Response({'chat_room_id': chat_room.chat_room_id}, status=201)


class SellerChatRoomListView(ListAPIView):
    permission_classes = [IsSeller]
    pagination_class = None

    def get_queryset(self):
        return ChatRoomRepository().get_chat_rooms_by_seller_id(self.request.user.seller.seller_id)

    def get_serializer_class(self):
        # TODO: 추후 default로 마지막 메세지만 보여주는 것으로 변경
        if self.request.query_params.get('only_last_message'):
            return SellerChatRoomListSerializer
        return SellerChatRoomListAllMessagesSerializer


class ChatRoomMessageListView(ListAPIView):
    permission_classes = [IsInChatRoom]
    serializer_class = MessageSerializer

    def list(self, request, *args, **kwargs):
        self.check_object_permissions(request, self.get_object())
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        return MessageRepository().get_messages_by_chat_room_uuid(
            chat_room_uuid=self.kwargs['chat_room_uuid'],
            message_uuid=self.request.query_params.get('message_uuid'),
        )

    def get_object(self):
        return ChatRoomRepository().get_chat_room_by_uuid(self.kwargs['chat_room_uuid'])


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


class MessageReadView(APIView):
    serializer_class = MessageReadSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        MessageService().read(
            user_id=request.user.user_id,
            chat_room_uuid=serializer.validated_data['chat_room_uuid'],
            message_uuid=serializer.validated_data['message_uuid'],
        )
        return Response(status=204)
