from typing import Optional

from django.db import transaction

from apps.users.models import User, UserOAuthInfo


class UserRepository:
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
    def signup(self, provider, provider_id, is_agree_privacy, is_agree_ads, nickname):
        user_info = User.objects.create(
            is_agree_privacy=is_agree_privacy,
            is_agree_ads=is_agree_ads,
            nickname=nickname,
            is_seller=False,
            is_staff=False
        )
        oauth_info = UserOAuthInfo.objects.create(
            user=user_info,
            provider=provider,
            provider_id=provider_id,
        )
        return user_info

    def check_nickname(self, nickname):
        if User.objects.filter(nickname=nickname).exists():
            return True
        return False
