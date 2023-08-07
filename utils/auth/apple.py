from datetime import datetime, timedelta

import jwt
import requests
from django.conf import settings
from jwt import PyJWKClient
from social_core.utils import handle_http_errors


class AppleOAuth2:
    name = "apple"
    APPLE_PUBLIC_KEY_URL = "https://appleid.apple.com/auth/keys"
    SCOPE_SEPARATOR = ","

    @handle_http_errors
    def do_auth(self, code, *args, **kwargs):
        """
        Finish the auth process once the access_token was retrieved
        Get the email from ID token received from apple
        """
        client_id, client_secret = self.get_key_and_secret()
        # start_index = code.index('code=')
        # extracted_code = code[start_index:]

        headers = {'content-type': "application/x-www-form-urlencoded"}
        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': 'https://dev.leporem.art/users/validate/apple',
        }
        """client secret 유효성 검사"""
        try:
            res = requests.post(self.APPLE_PUBLIC_KEY_URL, data=data, headers=headers)
            response_json = res.json()
            id_token = response_json.get('id_token')
            if not id_token:
                raise Exception("Invalid Token")
            jwks_client = PyJWKClient(res)
            signing_key = jwks_client.get_signing_key_from_jwt(id_token)
            decoded = jwt.decode(
                id_token,
                key=signing_key.key,
                audience=settings.APPLE_CONFIG["SOCIAL_AUTH_APPLE_ID_CLIENT"],
                algorithms=['RS256'],
                options={"verify_exp": False},
            )
            if (not decoded['sub']) or (not decoded['email']) or (not decoded['email_verified']):
                raise Exception("Invalid Token")

            response_data = {
                'sub': decoded['sub'],
                'email': decoded['email'],
                'email_verified': decoded['email_verified'],
            }

            return response_data
        except requests.exceptions.RequestException as e:
            print("Request error:", e)

        except requests.exceptions.RequestException as e:
            print("Request error:", e)
            raise Exception("Error during request to Apple API")

        except jwt.exceptions.DecodeError as decode_error:
            print("Decoding error:", decode_error)
            raise Exception("Error during JWT decoding")

        except Exception as e:
            print("General error:", e)
            raise Exception(e)

    def get_key_and_secret(self):
        """CREATE CLIENT_SECRET"""
        headers = {
            'alg': 'ES256',
            'kid': settings.APPLE_CONFIG.get('SOCIAL_AUTH_APPLE_ID_KEY'),
        }

        payload = {
            'iss': settings.APPLE_CONFIG.get('SOCIAL_AUTH_APPLE_ID_TEAM'),
            'iat': int(datetime.utcnow().timestamp()),
            'exp': int((datetime.utcnow() + timedelta(days=180)).timestamp()),
            'aud': "https://appleid.apple.com",
            'sub': settings.APPLE_CONFIG.get('SOCIAL_AUTH_APPLE_ID_CLIENT'),
        }

        client_secret = jwt.encode(
            payload, settings.APPLE_CONFIG.get('SOCIAL_AUTH_APPLE_ID_SECRET'), algorithm='ES256', headers=headers
        )

        return settings.APPLE_CONFIG.get('SOCIAL_AUTH_APPLE_ID_CLIENT'), client_secret
