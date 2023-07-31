from django.urls import path

from apps.chats.views import BuyerChatRoomListView, MessageCreateView

urlpatterns = [
    path('buyer', BuyerChatRoomListView.as_view()),
    path('messages', MessageCreateView.as_view()),
]
