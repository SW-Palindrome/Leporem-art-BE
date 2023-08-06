from typing import Optional

from django.db import transaction

from apps.users.models import User, UserOAuthInfo
from leporem_art import settings
from utils.files import create_random_filename


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

    def login_with_test_user(self):
        return User.objects.get(nickname=settings.TEST_STAFF_NICKNAME)

    @transaction.atomic
    def signup(self, provider, provider_id, is_agree_privacy, is_agree_ads, nickname):
        user_info = User.objects.create(
            is_agree_privacy=is_agree_privacy,
            is_agree_ads=is_agree_ads,
            nickname=nickname,
            is_seller=False,
            is_staff=False,
        )
        UserOAuthInfo.objects.create(
            user=user_info,
            provider=provider,
            provider_id=provider_id,
        )
        return user_info

    def check_nickname(self, nickname):
        if User.objects.filter(nickname=nickname).exists():
            return True
        return False

    def change_nickname(self, user_id, nickname):
        user = User.objects.get(user_id=user_id)
        user.nickname = nickname
        user.save()

    def change_profile_image(self, user_id, profile_image):
        profile_image.name = create_random_filename(profile_image.name)
        user = User.objects.get(user_id=user_id)
        user.profile_image = profile_image
        user.save()

    def check_is_staff(self, user_id):
        if User.objects.filter(pk=user_id, is_staff=True).exists():
            return True
        return False

    def remove(self, user_nickname):
        user = User.objects.get(nickname=user_nickname)
        if user.is_seller:
            user.seller.delete()
        user.delete()
        return True

    def get_user_info(self, user_id):
        user = User.objects.get(user_id=user_id)
        return user

    @transaction.atomic
    def apple_signup(self, provider, provider_id, refresh_token, is_agree_privacy, is_agree_ads, nickname):
        user_info = User.objects.create(
            is_agree_privacy=is_agree_privacy,
            is_agree_ads=is_agree_ads,
            nickname=nickname,
            is_seller=False,
            is_staff=False,
        )
        UserOAuthInfo.objects.create(
            user=user_info,
            provider=provider,
            provider_id=provider_id,
            refresh_token=refresh_token,
        )
        return user_info

    def get_token(self, user_id):
        return UserOAuthInfo.objects.get(user=user_id).values('refresh_token')
