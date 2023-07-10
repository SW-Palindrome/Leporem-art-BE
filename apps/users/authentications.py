from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from apps.users.models import User
from utils.auth.kakao import validate_id_token as kakao_validate_id_token, extract_provider_id as kakao_extract_provider_id


class OIDCAuthentication(BaseAuthentication):
    def authenticate(self, request):
        id_token = str(get_authorization_header(request).split()[-1])
        if not id_token:
            return None

        if kakao_validate_id_token(id_token):
            try:
                user = User.objects.get(
                    user_oauth_info__provider='KAKAO',
                    user_oauth_info__provider_id=kakao_extract_provider_id(id_token),
                )
            except User.DoesNotExist:
                raise AuthenticationFailed('No such user')

            return user, None
