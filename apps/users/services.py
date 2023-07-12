import re
from typing import Optional
from urllib.parse import urlencode

import requests

from apps.users.models import User
from apps.users.repositories import UserRepository


class AuthService:
    nickname_pattern = r'^[A-Za-z0-9가-힣_-]{2,10}$'

    def _check_nickname(self, nickname):
        user_repository = UserRepository()
        if not re.match(self.nickname_pattern, nickname):
            return False
        if user_repository.check_nickname(nickname):
            return False
        return True

    def signup(self, provider, provider_id, is_agree_privacy, is_agree_ads, nickname):
        user_repository = UserRepository()
        if not self._check_nickname(nickname):
            return False
        return user_repository.signup(provider, provider_id, is_agree_privacy, is_agree_ads, nickname)

    def login(self, provider, provider_id):
        user_repository = UserRepository()
        if not user_repository.login(provider, provider_id):
            return False
        return user_repository.login(provider, provider_id)

    def remove(self, user_nickname, staff_id):
        """회원 삭제"""
        user_repository = UserRepository()
        if not user_repository.check_is_staff(staff_id):
            return False
        return user_repository.remove(user_nickname)
