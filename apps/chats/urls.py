from django.urls import path

from apps.chats.views import (
    BuyerChatRoomView,
    ChatRoomMessageListView,
    MessageCreateView,
    SellerChatRoomListView,
)

urlpatterns = [
    path('buyer', BuyerChatRoomView.as_view()),
    path('seller', SellerChatRoomListView.as_view()),
    path('messages', MessageCreateView.as_view()),
    path('chat-rooms/<str:chat_room_uuid>/messages', ChatRoomMessageListView.as_view()),
]
