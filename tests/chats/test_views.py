from datetime import timedelta

import pytest
from django.utils import timezone

from apps.chats.models import Message
from tests.buyers.factories import BuyerFactory
from tests.chats.factories import ChatRoomFactory, MessageFactory
from tests.sellers.factories import SellerFactory
from tests.users.factories import UserFactory
from tests.utils import force_login


@pytest.mark.django_db
class TestBuyerChatRoomView:
    @pytest.fixture
    def user(self):
        return UserFactory()

    @pytest.fixture
    def user_sender(self):
        return UserFactory()

    @pytest.fixture
    def buyer(self, user):
        return BuyerFactory(user=user)

    @pytest.fixture
    def seller(self, user_sender):
        return SellerFactory(user=user_sender)

    @pytest.fixture
    def chat_room_1(self, buyer, seller):
        return ChatRoomFactory(buyer=buyer, seller=seller)

    @pytest.fixture
    def chat_room_2(self, buyer):
        return ChatRoomFactory(buyer=buyer)

    @pytest.fixture
    def messages_for_chat_room_1(self, user, buyer, user_sender, chat_room_1):
        MessageFactory.create_batch(5, chat_room=chat_room_1, user_id=user.user_id)
        MessageFactory.create_batch(5, chat_room=chat_room_1, user_id=user_sender.user_id)

    def test_get_chat_room_list(self, client, buyer, user, chat_room_1, chat_room_2):
        force_login(client, user)
        response = client.get('/chats/buyer')
        assert response.status_code == 200
        data = response.json()

        assert len(data) == 2
        assert data[0]['chat_room_id']
        assert data[0]['opponent_nickname']
        assert data[0]['opponent_user_id']
        assert data[0]['opponent_profile_image']
        assert data[0]['message_list']
        assert data[0]['uuid']

        message_list = data[0]['message_list']
        assert len(message_list) == 1
        assert message_list[0]['message_id']
        assert message_list[0]['user_id']
        assert message_list[0]['write_datetime']
        assert not message_list[0]['is_read']
        assert message_list[0]['message']
        assert message_list[0]['uuid']
        assert message_list[0]['type']

    def test_get_chat_room_list_show_only_last_message(
        self, client, user, buyer, chat_room_1, messages_for_chat_room_1
    ):
        force_login(client, user)
        response = client.get('/chats/buyer', {'only_last_message': True})
        assert response.status_code == 200
        data = response.json()

        assert len(data) == 1
        assert data[0]['unread_count'] == 5
        assert data[0]['last_message']
        assert not data[0].get('message_list')


@pytest.mark.django_db
class TestSellerChatRoomListView:
    @pytest.fixture
    def user(self):
        return UserFactory()

    @pytest.fixture
    def user_sender(self):
        return UserFactory()

    @pytest.fixture
    def buyer(self, user_sender):
        return BuyerFactory(user=user_sender)

    @pytest.fixture
    def seller(self, user):
        return SellerFactory(user=user)

    @pytest.fixture
    def chat_room_1(self, seller, buyer):
        return ChatRoomFactory(seller=seller, buyer=buyer)

    @pytest.fixture
    def messages_for_chat_room_1(self, user, user_sender, seller, chat_room_1):
        MessageFactory.create_batch(5, user_id=user.user_id, chat_room=chat_room_1)
        MessageFactory.create_batch(5, chat_room=chat_room_1, user_id=user_sender.user_id)

    @pytest.fixture
    def chat_room_2(self, seller):
        return ChatRoomFactory(seller=seller)

    @pytest.fixture
    def chat_room_as_buyer(self, buyer):
        return ChatRoomFactory(buyer=buyer)

    def test_get_chat_room_list(self, client, seller, chat_room_1, chat_room_2):
        user = seller.user
        force_login(client, user)
        response = client.get('/chats/seller')
        assert response.status_code == 200
        data = response.json()

        assert len(data) == 2
        assert data[0]['chat_room_id']
        assert data[0]['opponent_nickname']
        assert data[0]['opponent_user_id']
        assert data[0]['opponent_profile_image']
        assert data[0]['message_list']
        assert data[0]['uuid']

        message_list = data[0]['message_list']
        assert len(message_list) == 1
        assert message_list[0]['message_id']
        assert message_list[0]['user_id']
        assert message_list[0]['write_datetime']
        assert not message_list[0]['is_read']
        assert message_list[0]['message']
        assert message_list[0]['uuid']
        assert message_list[0]['type']

    def test_get_chat_room_list_with_buyer_not_included(self, client, seller, buyer, chat_room_1, chat_room_as_buyer):
        user = seller.user
        force_login(client, user)
        response = client.get('/chats/seller')
        assert response.status_code == 200
        data = response.json()

        assert len(data) == 1

    def test_get_chat_room_list_show_only_last_message(self, client, seller, chat_room_1, messages_for_chat_room_1):
        user = seller.user
        force_login(client, user)
        response = client.get('/chats/seller', {'only_last_message': True})
        assert response.status_code == 200
        data = response.json()

        assert len(data) == 1
        assert data[0]['unread_count'] == 6
        assert data[0]['last_message']
        assert not data[0].get('message_list')


@pytest.mark.django_db
class TestChatRoomMessageListView:
    @pytest.fixture
    def user(self):
        return UserFactory()

    @pytest.fixture
    def user_not_in_chat_room(self):
        return UserFactory()

    @pytest.fixture
    def buyer(self, user):
        return BuyerFactory(user=user)

    @pytest.fixture
    def chat_room(self, buyer):
        return ChatRoomFactory(buyer=buyer)

    @pytest.fixture
    def messages(self, chat_room):
        messages = []
        first_message = chat_room.last_message
        write_datetime = timezone.now() - timedelta(days=10)
        first_message.write_datetime = write_datetime
        first_message.save()
        messages.append(first_message)
        for _ in range(30):
            write_datetime += timedelta(minutes=1)
            messages.append(MessageFactory(chat_room=chat_room, write_datetime=write_datetime))
        return messages

    def test_list_messages(self, client, user, buyer, chat_room, messages):
        force_login(client, user)
        response = client.get(f'/chats/chat-rooms/{chat_room.uuid}/messages')
        assert response.status_code == 200
        data = response.json()

        assert data['count'] == 31

    def test_list_messages_with_user_not_in_chat_room(self, client, user_not_in_chat_room, chat_room):
        force_login(client, user_not_in_chat_room)
        response = client.get(f'/chats/chat-rooms/{chat_room.uuid}/messages')
        assert response.status_code == 403

    def test_list_messages_with_message_uuid(self, client, user, buyer, chat_room, messages):
        force_login(client, user)
        message = messages[5]
        response = client.get(f'/chats/chat-rooms/{chat_room.uuid}/messages', {'message_uuid': message.uuid})
        assert response.status_code == 200
        data = response.json()

        assert data['count'] == 5


@pytest.mark.django_db
class TsetMessageReadView:
    @pytest.fixture
    def user_message_sender(self):
        return UserFactory()

    @pytest.fixture
    def user_message_receiver(self):
        return UserFactory()

    @pytest.fixture
    def seller(self, user_message_receiver):
        return SellerFactory(user=user_message_receiver)

    @pytest.fixture
    def buyer(self, user_message_sender):
        return BuyerFactory(user=user_message_sender)

    @pytest.fixture
    def chat_room(self, buyer, seller):
        return ChatRoomFactory(buyer=buyer, seller=seller)

    @pytest.fixture
    def message(self, chat_room, user_message_sender):
        return MessageFactory(chat_room=chat_room, user_id=user_message_sender.user_id)

    def test_set_message_read(self, client, user_message_receiver, message):
        force_login(client, user_message_receiver)
        assert Message.objects.filter(is_read=False).count() == 2
        response = client.patch('/chats/messages/read', data={'message_uuid': message.uuid})
        assert response.status_code == 200
        assert Message.objects.filter(is_read=False).count() == 0
