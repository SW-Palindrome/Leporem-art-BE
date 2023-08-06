import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from apps.users.repositories import UserRepository
from apps.users.services import AuthService


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
        try:
            token = request.headers.get("AUTHORIZATION")
            if not token:
                return None
            decoded = jwt.decode(token, settings.JWT_AUTH.get("JWT_SECRET_KEY"), algorithms=["HS256"])
            provider = decoded.get("provider")
            email = decoded.get("email")
            user = UserRepository().login(provider, email)
            return user, None
        except jwt.exceptions.DecodeError:
            msg = {
                "message": "Invalid Token",
                "code": "JWT_403_INVALID_ACCESSTOKEN",
            }
            raise AuthenticationFailed(msg)
        except jwt.ExpiredSignatureError:
            msg = {
                "message": "Expired Token",
                "code": "JWT_403_EXPIRED_ACCESSTOKEN",
            }
            raise AuthenticationFailed(msg)
