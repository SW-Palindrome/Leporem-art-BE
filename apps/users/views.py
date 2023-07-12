from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.services import AuthService
from utils.auth.kakao import extract_provider_id

from .permissions import IsStaff


# Create your views here.
class KakaoSignUpView(APIView):
    """회원가입: 이용약관동의여부, 닉네임"""

    PROVIDER = 'KAKAO'
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        provider_id = extract_provider_id(request.data.get('id_token'))
        is_agree_privacy = request.data.get('is_agree_privacy')
        is_agree_ads = request.data.get('is_agree_ads')
        nickname = request.data.get('nickname')
        auth_service = AuthService()
        if not auth_service.signup(self.PROVIDER, provider_id, is_agree_privacy, is_agree_ads, nickname):
            return Response({'message': 'signup failed'}, status=400)

        return Response({'message': 'success'}, status=201)


class KakaoLogInView(APIView):
    """로그인: 최초회원가입 이후 재로그인"""

    def get(self, request):
        auth_service = AuthService()
        provider = request.data.get('provider')
        provider_id = extract_provider_id(request.data.get('id_token'))
        if not auth_service.login(provider, provider_id):
            return Response({'message': 'signin failed'}, status=401)
        return Response({'message': 'success'}, status=200)


class ValidateNicknameView(APIView):
    """닉네임 검증 API"""

    def get(self, request, *args, **kwargs):
        nickname = kwargs['nickname']
        auth_service = AuthService()
        if not auth_service.check_nickname(nickname):
            return Response({'message': 'invalid nickname'}, status=400)
        return Response({'message': 'success'}, status=200)


class RemoveUserView(APIView):
    permission_classes = [IsStaff]

    def delete(self, request):
        auth_service = AuthService()
        if not auth_service.remove(request.data['nickname'], request.user.user_id):
            return Response({'message': 'remove user failed'}, status=400)
        return Response({'message': 'success'}, status=200)
