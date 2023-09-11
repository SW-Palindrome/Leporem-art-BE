import uuid

import pytest

from apps.buyers.models import Buyer
from apps.chats.models import ChatRoom
from apps.chats.repositories import ChatRoomRepository
from apps.sellers.models import Seller
from apps.users.models import User


@pytest.mark.django_db
class TestChatRoomRepository:
    @pytest.fixture
    def buyer(self):
        user = User.objects.create(
            nickname='구매자',
            is_seller=False,
            is_staff=False,
        )
        return Buyer.objects.create(user=user)

    @pytest.fixture
    def seller(self):
        user = User.objects.create(
            nickname='판매자',
            is_seller=True,
            is_staff=False,
        )
        return Seller.objects.create(user=user)

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
