import factory

from apps.buyers.models import Buyer


class BuyerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Buyer

    user = factory.SubFactory('tests.users.factories.UserFactory')
