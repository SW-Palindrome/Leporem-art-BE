import uuid

import pytest

from apps.chats.models import ChatRoom
from apps.chats.repositories import ChatRoomRepository
from tests.buyers.factories import BuyerFactory
from tests.sellers.factories import SellerFactory


@pytest.mark.django_db
class TestChatRoomRepository:
    @pytest.fixture
    def buyer(self):
        return BuyerFactory()

    @pytest.fixture
    def seller(self):
        return SellerFactory()

    def test_create_by_buyer(self, buyer, seller):
        ChatRoomRepository().create_by_buyer(
            buyer_id=buyer.buyer_id,
            seller_id=seller.seller_id,
        )
        assert ChatRoom.objects.count() == 1

    def test_create_by_buyer_with_uuid(self, buyer, seller):
        chat_room_uuid = uuid.uuid4()
        ChatRoomRepository().create_by_buyer(
            buyer_id=buyer.buyer_id,
            seller_id=seller.seller_id,
            chat_room_uuid=chat_room_uuid,
        )
        assert ChatRoom.objects.count() == 1
        assert ChatRoom.objects.filter(uuid=chat_room_uuid).exists()
