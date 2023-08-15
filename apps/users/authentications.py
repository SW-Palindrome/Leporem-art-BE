from rest_framework.authentication import BaseAuthentication

from utils.auth.leporemart import validate_token


class OIDCAuthentication(BaseAuthentication):
    def authenticate(self, request):
        user = validate_token(request)
        return user, None
