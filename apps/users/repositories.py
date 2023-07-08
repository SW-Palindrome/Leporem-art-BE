from typing import Optional

from django.db import transaction

from apps.users.models import User, UserOAuthInfo


class UserRepository:
    @transaction.atomic
    def signup(self, provider, email, nickname):
        user = User.objects.create(nickname=nickname)
        UserOAuthInfo.objects.create(
            user=user,
            provider=provider,
            provider_id=email,
        )
        return user

    def login(self, provider, email) -> Optional[User]:
        try:
            user_oauth_info = UserOAuthInfo.objects.get(
                provider=provider,
                provider_id=email,
            )
            return user_oauth_info.user
        except UserOAuthInfo.DoesNotExist:
            return None

    @transaction.atomic
    def kakao_signup(self, provider, provider_id, nickname):
        kakao_oauth_info = UserOAuthInfo.objects.create(provider=provider, provider_id=provider_id)
        kakao_oauth_info.save()
        user = User.objects.create(nickname=nickname)
        user.save()
        return user

    def kakao_signin(self, provider, provider_id):
        try:
            kakao_oauth_info = UserOAuthInfo.objects.get(
                provider=provider,
                provider_id=provider_id,
            )
            return kakao_oauth_info.user
        except UserOAuthInfo.DoesNotExist:
            return None
