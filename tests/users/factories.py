import factory

from apps.users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    nickname = factory.Sequence(lambda n: f'사용자{n}')
    inactive_datetime = None
    is_agree_privacy = True
    is_agree_terms = True
    is_agree_ads = True
    is_seller = False
    is_staff = False
