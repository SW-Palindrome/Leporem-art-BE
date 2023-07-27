from django.urls import path

from apps.chats.views import BuyerChatRoomListView

urlpatterns = [
    path('buyer', BuyerChatRoomListView.as_view()),
]
