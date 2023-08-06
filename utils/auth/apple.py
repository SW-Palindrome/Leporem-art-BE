from datetime import datetime, timedelta

import jwt
import requests
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from social_core.utils import handle_http_errors

from apps.users.repositories import UserRepository


class AppleOAuth2:
    name = "apple"
    ACCESS_TOKEN_URL = "https://appleid.apple.com/auth/token"
    SCOPE_SEPARATOR = ","

    @handle_http_errors
    def do_auth(self, code, *args, **kwargs):
        """
        Finish the auth process once the access_token was retrieved
        Get the email from ID token received from apple
        """
        client_id, client_secret = self.get_key_and_secret()

        headers = {'content-type', "application/x-www-form-urlencoded"}
        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': 'https://dev.leporem.art/users/login/apple',
        }
        """client secret 유효성 검사"""
        res = requests.post(AppleOAuth2.ACCESS_TOKEN_URL, data=data, headers=headers)
        response_dict = res.json()
        id_token = response_dict.get('id_token', None)

        if not id_token:
            raise Exception("Invalid Token")

        decoded = jwt.decode(id_token, verify=False)
        if (not decoded.get('sub')) or (not decoded.get('email')) or (not decoded.get('email_verified')):
            raise Exception("Invalid Token")

        response_data = {
            'sub': decoded.get('sub'),
            'email': decoded.get('email'),
            'email_verified': decoded.get('email_verified'),
        }

        return response_data

    def get_key_and_secret(self):
        """CREATE CLIENT_SECRET"""
        headers = {
            'alg': 'ES256',
            'kid': settings.APP_CONFIG.get('SOCIAL_AUTH_APPLE_ID_KEY'),
        }

        payload = {
            'iss': settings.APP_CONFIG.get('SOCIAL_AUTH_APPLE_ID_TEAM'),
            'iat': int(datetime.now().timestamp()),
            'exp': int(datetime.now() + timedelta(days=180)).timestamp(),
            'aud': "https://appleid.apple.com",
            'sub': settings.APP_CONFIG.get('SOCIAL_AUTH_APPLE_ID_CLIENT'),
        }

        client_secret = jwt.encode(
            payload, settings.APP_CONFIG.get('SOCIAL_AUTH_APPLE_PRIVATE_KEY'), algorithms='ES256', headers=headers
        ).decode("utf-8")

        return settings.APP_CONFIG.get('SOCIAL_AUTH_APPLE_ID_CLIENT'), client_secret


def generate_access_token(payload, type):
    if type == "access":
        exp = datetime.now() + timedelta(hours=3)
    elif type == "refresh":
        exp = datetime.now() + timedelta(days=180)
    else:
        raise Exception("Invalid token type.")

    token_payload = {
        'user_id': payload.user_id,
        'exp': exp,
        'iat': datetime.now(),
    }

    token = jwt.encode(token_payload, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM).decode('utf-8')

    return token


def validate_token(request):
    try:
        token = request.headers.get("AUTHORIZATION")
        if not token:
            return None
        decoded = jwt.decode(token, settings.JWT_AUTH.get("JWT_SECRET_KEY"), algorithms=["HS256"])
        provider = decoded.get("provider")
        email = decoded.get("email")
        user = UserRepository().apple_login(provider, email)
        return user, None
    except jwt.exceptions.DecodeError:
        msg = {
            "message": "잘못된 토큰입니다.",
            "code": "JWT_403_INVALID_ACCESSTOKEN",
        }
        raise AuthenticationFailed(msg)
    except jwt.ExpiredSignatureError:
        msg = {
            "message": "토큰이 만료되었습니다.",
            "code": "JWT_403_EXPIRED_ACCESSTOKEN",
        }
        raise AuthenticationFailed(msg)


def refresh_token(request):
    try:
        refresh_token = request.headers.get('refresh_token')
        if not refresh_token:
            msg = {
                "message": "refresh_token을 보내주세요.",
                "code": "JWT_400_NOT_FOUND_TOKEN",
            }
            raise AuthenticationFailed(msg)
        decoded = jwt.decode(refresh_token, settings.JWT_AUTH("JWT_SECRET_KEY"), settings.JWT_AUTH("JWT_ALGORITHM"))

        payload = {'provider': decoded.get("provider"), 'email': decoded.get("email")}
        access_token = generate_access_token(payload, "access")
        refresh_token = generate_access_token(payload, "refresh")

        return {"email": decoded.get("email"), "access_token": access_token, "refresh_token": refresh_token}
    except jwt.ExpiredSignatureError:
        msg = {
            "message": "refresh_token이 만료되었습니다.",
            "code": "JWT_401_TOKEN_EXPIRED",
        }
        raise AuthenticationFailed(msg)
