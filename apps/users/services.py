import re
from typing import Optional

from django.conf import settings
from django.db import IntegrityError
from rest_framework.exceptions import AuthenticationFailed

from apps.buyers.respositories import BuyerRepository
from apps.users.exceptions import (
    DuplicateNicknameException,
    DuplicateUserInfoException,
    ExpiredTokenException,
)
from apps.users.models import User
from apps.users.repositories import UserRepository
from utils.auth.kakao import extract_provider_id as kakao_extract_provider_id
from utils.auth.kakao import validate_id_token as kakao_validate_id_token


class AuthService:
    nickname_pattern = r'^[A-Za-z0-9가-힣_-]{2,10}$'

    def check_nickname(self, nickname):
        user_repository = UserRepository()
        if not re.match(self.nickname_pattern, nickname):
            return False
        if user_repository.check_nickname(nickname):
            return False
        return True

    def change_nickname(self, user_id, nickname):
        if self.check_nickname(nickname):
            user_repository = UserRepository()
            user_repository.change_nickname(user_id, nickname)
            return True
        return False

    def login(self, id_token) -> Optional[User]:
        user_repository = UserRepository()

        if not id_token:
            return None

        user = None

        if id_token == settings.TEST_ID_TOKEN:
            user = user_repository.login_with_test_user()

        try:
            is_kakao_id_token = kakao_validate_id_token(id_token)
        except ExpiredTokenException:
            raise AuthenticationFailed('Expired token')

        if is_kakao_id_token:
            user = user_repository.login('KAKAO', kakao_extract_provider_id(id_token))
            if user is None:
                raise AuthenticationFailed('No such user')

        return user

    def signup(self, provider, provider_id, refresh_token, is_agree_privacy, is_agree_terms, is_agree_ads, nickname):
        user_repository = UserRepository()
        buyer_repository = BuyerRepository()
        if not self.check_nickname(nickname):
            raise DuplicateNicknameException
        try:
            user = user_repository.signup(
                provider, provider_id, refresh_token, is_agree_privacy, is_agree_terms, is_agree_ads, nickname
            )
        except IntegrityError:
            raise DuplicateUserInfoException
        buyer_repository.register(user.user_id)
        return True


class UserService:
    def change_profile_image(self, user_id, profile_image):
        user_repository = UserRepository()
        user_repository.change_profile_image(user_id, profile_image)

    def inactive(self, user_id):
        user_repository = UserRepository()
        user_repository.inactive(user_id)
