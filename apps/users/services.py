import re

from django.db import IntegrityError

from apps.users.exceptions import DuplicateNicknameException, DuplicateUserInfoException
from apps.users.repositories import UserRepository


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

    def signup(self, provider, provider_id, is_agree_privacy, is_agree_ads, nickname):
        user_repository = UserRepository()
        if not self.check_nickname(nickname):
            raise DuplicateNicknameException
        try:
            user_repository.signup(provider, provider_id, is_agree_privacy, is_agree_ads, nickname)
        except IntegrityError:
            raise DuplicateUserInfoException
        return True

    def login(self, provider, provider_id):
        user_repository = UserRepository()
        if not user_repository.login(provider, provider_id):
            return False
        return user_repository.login(provider, provider_id)


class UserService:

    def change_profile_image(self, user_id, profile_image):
        user_repository = UserRepository()
        user_repository.change_profile_image(user_id, profile_image)

    def get_user_info(self, user_id):
        user_repository = UserRepository()
        return user_repository.get_user_info(user_id)

    def remove(self, user_nickname, staff_id):
        """회원 삭제"""
        user_repository = UserRepository()
        if not user_repository.check_is_staff(staff_id):
            return False
        return user_repository.remove(user_nickname)
