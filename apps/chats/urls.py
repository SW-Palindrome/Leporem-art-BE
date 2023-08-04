from django.urls import path

from apps.chats.views import (
    BuyerChatRoomListView,
    MessageCreateView,
    SellerChatRoomListView,
)

urlpatterns = [
    path('buyer', BuyerChatRoomListView.as_view()),
    path('seller', SellerChatRoomListView.as_view()),
    path('messages', MessageCreateView.as_view()),
]
