import factory

from apps.sellers.models import Seller


class SellerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Seller

    user = factory.SubFactory('tests.users.factories.UserFactory', is_seller=True)
