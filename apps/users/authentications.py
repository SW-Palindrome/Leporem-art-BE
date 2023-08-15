from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from apps.users.services import AuthService
from utils.auth.leporemart import validate_token


class OIDCAuthentication(BaseAuthentication):
    def authenticate(self, request):
        """kakao login user"""
        auth = get_authorization_header(request).split()

        if auth and auth[0].lower() == b'palindrome':
            if len(auth) == 1:
                msg = 'Invalid basic header. No credentials provided.'
                raise AuthenticationFailed(msg)
            elif len(auth) > 2:
                msg = 'Invalid basic header. Credentials string should not contain spaces.'
                raise AuthenticationFailed(msg)

            id_token = auth[1]

            if isinstance(id_token, bytes):
                id_token = id_token.decode('utf-8')

            user = AuthService().login(id_token)

            return user, None

        """apple login user"""
        user = validate_token(request)
        return user, None
