from django.urls import path

from apps.chats.views import (
    BuyerChatRoomView,
    MessageCreateView,
    SellerChatRoomListView,
)

urlpatterns = [
    path('buyer', BuyerChatRoomView.as_view()),
    path('seller', SellerChatRoomListView.as_view()),
    path('messages', MessageCreateView.as_view()),
]
