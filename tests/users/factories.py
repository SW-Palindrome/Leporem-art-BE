import factory

from apps.users.models import User, UserOAuthInfo


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

    @factory.post_generation
    def oauth_info(self, create, extracted, **kwargs):
        if not create:
            return

        UserOAuthInfoFactory(user=self, **kwargs)


class UserOAuthInfoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserOAuthInfo

    user = factory.SubFactory(UserFactory)
    provider = 'kakao'
    provider_id = factory.Sequence(lambda n: f'kakao_id{n}')
