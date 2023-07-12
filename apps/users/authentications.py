from django.conf import settings
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from apps.users.models import User
from utils.auth.kakao import extract_provider_id as kakao_extract_provider_id
from utils.auth.kakao import validate_id_token as kakao_validate_id_token


class OIDCAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'palindrome':
            return None

        if len(auth) == 1:
            msg = 'Invalid basic header. No credentials provided.'
            raise AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid basic header. Credentials string should not contain spaces.'
            raise AuthenticationFailed(msg)

        id_token = auth[1]

        if isinstance(id_token, bytes):
            id_token = id_token.decode('utf-8')

        if not id_token:
            return None

        if settings.DEBUG and id_token == settings.TEST_ID_TOKEN:
            return User.objects.get(nickname=settings.TEST_STAFF_NICKNAME), None

        if kakao_validate_id_token(id_token):
            try:
                user = User.objects.get(
                    user_oauth_info__provider='KAKAO',
                    user_oauth_info__provider_id=kakao_extract_provider_id(id_token),
                )
            except User.DoesNotExist:
                raise AuthenticationFailed('No such user')

            return user, None
