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
