import factory.django

from apps.chats.models import ChatRoom, Message


class ChatRoomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ChatRoom

    buyer = factory.SubFactory('tests.buyers.factories.BuyerFactory')
    seller = factory.SubFactory('tests.sellers.factories.SellerFactory')

    @factory.post_generation
    def message(self, create, extracted, **kwargs):
        if not create:
            return

        return MessageFactory(chat_room=self, user_id=self.buyer.user_id)


class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message

    chat_room = factory.SubFactory(ChatRoomFactory)
    user = factory.SubFactory('tests.users.factories.UserFactory')
    is_read = False
    text = factory.Faker('sentence')
    image = None
    type = Message.Type.TEXT
