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