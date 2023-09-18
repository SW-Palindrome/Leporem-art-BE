import pytest

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
    def buyer(self, user):
        return BuyerFactory(user=user)

    @pytest.fixture
    def chat_room_1(self, buyer):
        return ChatRoomFactory(buyer=buyer)

    @pytest.fixture
    def chat_room_2(self, buyer):
        return ChatRoomFactory(buyer=buyer)

    @pytest.fixture
    def messages_for_chat_room_1(self, chat_room_1):
        return MessageFactory.create_batch(5, chat_room=chat_room_1)

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
        assert data[0]['last_message']
        assert not data[0].get('message_list')


@pytest.mark.django_db
class TestSellerChatRoomListView:
    @pytest.fixture
    def user(self):
        return UserFactory()

    @pytest.fixture
    def buyer(self, user):
        return BuyerFactory(user=user)

    @pytest.fixture
    def seller(self, user):
        return SellerFactory(user=user)

    @pytest.fixture
    def chat_room_1(self, seller):
        return ChatRoomFactory(seller=seller)

    @pytest.fixture
    def messages_for_chat_room_1(self, chat_room_1):
        return MessageFactory.create_batch(5, chat_room=chat_room_1)

    @pytest.fixture
    def chat_room_2(self, seller):
        return ChatRoomFactory(seller=seller)

    @pytest.fixture
    def chat_room_as_buyer(self, seller, buyer):
        return ChatRoomFactory(buyer=seller.user.buyer)

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
        assert data[0]['last_message']
        assert not data[0].get('message_list')
