import factory

from apps.sellers.models import Seller


class SellerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Seller

    user = factory.SubFactory('tests.users.factories.UserFactory')

    @factory.post_generation
    def is_seller(self, *args, **kwargs):
        self.user.is_seller = True
        self.user.save()
