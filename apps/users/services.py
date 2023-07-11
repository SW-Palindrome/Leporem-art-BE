import re
from typing import Optional
from urllib.parse import urlencode

import requests

from apps.users.models import User
from apps.users.repositories import UserRepository


class GoogleAuthService:
    """구글 oAuth 인증을 위한 서비스"""

    CLIENT_ID = '380758119953-elpcovkkphuok64koqfprla0q1sj08v9.apps.googleusercontent.com'
    CLIENT_SECRET = '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'
    REDIRECT_URI = 'http://localhost:8000/auth/login/google'
    RESPONSE_TYPE = 'code'
    SCOPE = 'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email'
    ACCESS_TYPE = 'offline'
    AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
    TOKEN_URL = 'https://oauth2.googleapis.com/token'
    PROFILE_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'
    PROVIDER = 'GOOGLE'

    def get_auth_url(self) -> str:
        """구글 oAuth 인증 URL을 반환합니다."""
        params = {
            'client_id': self.CLIENT_ID,
            'redirect_uri': self.REDIRECT_URI,
            'response_type': self.RESPONSE_TYPE,
            'scope': self.SCOPE,
            'access_type': self.ACCESS_TYPE,
        }
        return f'{self.AUTH_URL}?{urlencode(params)}'

    def _get_access_token(self, code) -> str:
        data = {
            'code': code,
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'redirect_uri': self.REDIRECT_URI,
        }
        response = requests.post(self.TOKEN_URL, data=data)
        return response.json()['access_token']

    def _get_email(self, access_token) -> str:
        params = {'access_token': access_token}
        response = requests.get(f'{self.PROFILE_URL}?{urlencode(params)}')
        return response.json()['email']

    def signup(self, code) -> User:
        """구글 oAuth 인증 후 회원가입을 처리합니다."""
        access_token = self._get_access_token(code)
        email = self._get_email(access_token)

        user_repository = UserRepository()
        # 최초에 nickname은 email을 사용한다.
        return user_repository.signup(self.PROVIDER, email, email)

    def login(self, code) -> Optional[User]:
        """구글 oAuth 인증 후 로그인을 처리합니다."""
        access_token = self._get_access_token(code)
        email = self._get_email(access_token)

        user_repository = UserRepository()
        return user_repository.login(self.PROVIDER, email)


class KakaoAuthService:
    PROVIDER = 'KAKAO'
    nickname_pattern = r'^[A-Za-z0-9가-힣_-]{2,10}$'

    def _check_nickname(self, nickname):
        user_repository = UserRepository()
        if not re.match(self.nickname_pattern, nickname):
            return False
        if user_repository.check_nickname(nickname):
            return False
        return True

    def signup(self, provider_id, is_agree_privacy, is_agree_ads, nickname):
        user_repository = UserRepository()
        if not self._check_nickname(nickname):
            return False
        return user_repository.signup(self.PROVIDER, provider_id, is_agree_privacy, is_agree_ads, nickname)

    def signin(self, provider_id):
        user_repository = UserRepository()
        if not user_repository.signin(provider_id):
            return False
        return user_repository.signin(provider_id)
