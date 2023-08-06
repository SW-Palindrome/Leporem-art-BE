from datetime import datetime, timedelta

import jwt
import requests
from django.conf import settings
from social_core.utils import handle_http_errors


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
