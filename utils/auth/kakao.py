import base64
import binascii
import json
from datetime import datetime

import jwt
from jwt import PyJWKClient

AUDIENCE = '8aeac9bb18f42060a2332885577b8cb9'


def validate_id_token(id_token: str) -> bool:
    """카카오 ID 토큰을 검증합니다.

    참고: https://developers.kakao.com/docs/latest/ko/kakaologin/common#oidc
    1. 페이로드를 Base64 방식으로 디코딩
    2. 페이로드의 iss 값이 https://kauth.kakao.com와 일치하는지 확인
    3. 페이로드의 aud 값이 서비스 앱 키와 일치하는지 확인
    4. 페이로드의 exp 값이 현재 UNIX 타임스탬프(Timestamp)보다 큰 값인지 확인(ID 토큰이 만료되지 않았는지 확인)
    5. 페이로드의 nonce 값이 카카오 로그인 요청 시 전달한 값과 일치하는지 확인
    6. 서명 검증
        1. 헤더를 Base64 방식으로 디코딩
        2. OIDC: 공개키 목록 조회하기를 통해 카카오 인증 서버가 서명 시 사용하는 공개키 목록 조회
            https://kauth.kakao.com/.well-known/jwks.json
        3. 공개키 목록에서 헤더의 kid에 해당하는 공개키 값 확인
            공개키는 일정 기간 캐싱(Caching)하여 사용할 것을 권장하며, 지나치게 빈번한 요청 시 요청이 차단될 수 있으므로 유의
        4. JWT 서명 검증을 지원하는 라이브러리를 사용해 공개키로 서명 검증
    """

    header, payload, signature = id_token.split('.')
    try:
        decoded_payload = json.loads(base64.urlsafe_b64decode(payload + '=' * (-len(payload) % 4)))
    except binascii.Error:
        return False

    if decoded_payload['iss'] != 'https://kauth.kakao.com':
        return False

    if decoded_payload['aud'] != AUDIENCE:
        return False

    if decoded_payload['exp'] < int(datetime.now().timestamp()):
        return False

    url = 'https://kauth.kakao.com/.well-known/jwks.json'

    jwks_client = PyJWKClient(url)
    signing_key = jwks_client.get_signing_key_from_jwt(id_token)
    try:
        jwt.decode(
            id_token,
            signing_key.key,
            algorithms=['RS256'],
            audience=AUDIENCE,
            options={"verify_exp": False},
        )
    except jwt.exceptions.InvalidSignatureError:
        return False

    return True


def extract_provider_id(id_token: str):
    """카카오 ID 토큰에서 고유 식별자를 추출합니다."""
    header, payload, signature = id_token.split('.')
    decoded_payload = json.loads(base64.urlsafe_b64decode(payload + '=' * (-len(payload) % 4)))
    return decoded_payload['sub']
