from datetime import datetime, timedelta

import jwt
from django.conf import settings
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from apps.users.repositories import UserRepository


def generate_access_token(provider, provider_id, kind):
    if kind == "access":
        exp = datetime.now() + timedelta(hours=3)
    elif kind == "refresh":
        exp = datetime.now() + timedelta(days=180)
    else:
        raise Exception("Invalid token type.")

    token_payload = {
        'provider': provider,
        'email': provider_id,
        'exp': int(exp.timestamp()),
        'iat': int(datetime.now().timestamp()),
    }
    key = settings.JWT_AUTH['JWT_SECRET_KEY'].encode('utf-8')
    token = jwt.encode(token_payload, key, settings.JWT_AUTH['JWT_ALGORITHM'])

    return token, token_payload['exp']


def validate_token(request):
    header = get_authorization_header(request)
    if not header:
        return None

    auth, token = header.split()

    if auth.lower() != b"bearer":
        raise AuthenticationFailed("Invalid token header. No credentials provided.")

    try:
        decoded = jwt.decode(token, settings.JWT_AUTH.get("JWT_SECRET_KEY"), algorithms=["HS256"])
        provider = decoded.get("provider")
        email = decoded.get("email")
        user = UserRepository().login(provider, email)
        return user
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
    user_repository = UserRepository()
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

        if decoded.get('exp') < int(datetime.now().timestamp()):
            if user_repository.get_token(request.user.user_id) == refresh_token:
                access_token = generate_access_token(payload, "access")
                refresh_token = generate_access_token(payload, "refresh")
                user_repository.refresh_token(request.user.user_id, refresh_token)
            else:
                raise AuthenticationFailed({"message": "토큰이 일치하지 않습니다."})
        else:
            access_token = generate_access_token(payload, "access")

        return {"access_token": access_token, "refresh_token": refresh_token}
    except jwt.exceptions.DecodeError:
        msg = {
            "message": "잘못된 토큰입니다.",
            "code": "JWT_403_INVALID_ACCESSTOKEN",
        }
        raise AuthenticationFailed(msg)
