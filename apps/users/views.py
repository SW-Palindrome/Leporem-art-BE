from django.conf import settings
from django.shortcuts import redirect
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.repositories import UserRepository
from apps.users.services import AuthService, UserService
from utils.auth.apple import AppleOAuth2
from utils.auth.kakao import extract_provider_id
from utils.auth.leporemart import generate_access_token, refresh_token, validate_token

from .exceptions import DuplicateNicknameException, DuplicateUserInfoException
from .permissions import IsStaff
from .serializers import ChangeNicknameSerializer, ChangeProfileImageSerializer


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

        try:
            auth_service.signup(self.PROVIDER, provider_id, is_agree_privacy, is_agree_ads, nickname)
        except DuplicateNicknameException:
            return Response({'message': 'duplicate nickname'}, status=400)
        except DuplicateUserInfoException:
            return Response({'message': 'duplicate user info'}, status=400)

        return Response({'message': 'success'}, status=201)


class KakaoLogInView(APIView):
    """로그인: 최초회원가입 이후 재로그인"""

    PROVIDER = 'KAKAO'
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        auth_service = AuthService()
        user = auth_service.login(id_token=request.data.get('id_token'))
        if user is None:
            return Response({'message': 'signin failed'}, status=401)
        return Response({'user_id': user.user_id, 'is_seller': user.is_seller, 'nickname': user.nickname}, status=200)


class ValidateNicknameView(APIView):
    """닉네임 검증 API"""

    def get(self, request, *args, **kwargs):
        nickname = kwargs['nickname']
        auth_service = AuthService()
        if not auth_service.check_nickname(nickname):
            return Response({'message': 'invalid nickname'}, status=400)
        return Response({'message': 'success'}, status=200)


class ChangeNicknameView(APIView):
    """닉네임 변경 API"""

    permission_classes = [IsAuthenticated]
    serializer_class = ChangeNicknameSerializer

    def patch(self, request):
        auth_service = AuthService()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not auth_service.change_nickname(request.user.user_id, serializer.validated_data['nickname']):
            return Response({'message': 'change nickname failed'}, status=400)
        return Response({'message': 'success'}, status=200)


class ChangeProfileImageView(APIView):
    """프로필 이미지 변경 API"""

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]
    serializer_class = ChangeProfileImageSerializer

    def patch(self, request):
        user_service = UserService()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_service.change_profile_image(request.user.user_id, serializer.validated_data['profile_image'])
        return Response({'message': 'success'}, status=200)


class RemoveUserView(APIView):
    permission_classes = [IsStaff]

    def delete(self, request):
        user_service = UserService()
        if not user_service.remove(request.data['nickname'], request.user.user_id):
            return Response({'message': 'remove user failed'}, status=400)
        return Response({'message': 'success'}, status=200)


class AppleLoginUrlView(APIView):
    permission_classes = [permissions.AllowAny]

    APPLE_BASE_URL = "https://appleid.apple.com"
    APPLE_AUTH_URL = f"{APPLE_BASE_URL}/auth/authorize"

    def get(self, request):
        client_id = settings.APPLE_CONFIG.get('SOCIAL_AUTH_APPLE_ID_CLIENT')
        redirect_uri = 'https://dev.leporem.art/users/validate/apple'
        uri = f"{self.APPLE_AUTH_URL}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}"

        res = redirect(uri)
        return res


class AppleLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    PROVIDER = "APPLE"

    def get(self, request):
        data = request.query_params
        code = data.get('code')

        apple_oauth = AppleOAuth2()
        user_details = apple_oauth.do_auth(code)

        user_repository = UserRepository()
        if user_repository.login(self.PROVIDER, user_details.get('sub')):
            if validate_token(data.get('access_token')):
                return Response({"message": "login successful"}, status=200)
        return Response({"message": "signup required", "data": user_details}, status=404)


class AppleSignUpView(APIView):
    permission_classes = [permissions.AllowAny]

    PROVIDER = "APPLE"

    def post(self, request):
        """자체 token, refresh token 생성 필요"""
        user_details = request.data.get('user_details')
        is_agree_privacy = request.data.get('is_agree_privacy')
        is_agree_ads = request.data.get('is_agree_ads')
        nickname = request.data.get('nickname')

        auth_service = AuthService()

        payload = {'provider': self.PROVIDER, 'email': user_details['sub']}

        try:
            access_token = generate_access_token(payload, "access")
            refresh_token = generate_access_token(payload, "refresh")
            auth_service.apple_signup(
                self.PROVIDER, user_details['sub'], refresh_token, is_agree_privacy, is_agree_ads, nickname
            )
            response_data = {
                'email': user_details['sub'],
                'access_token': access_token,
                'refresh_token': refresh_token,
            }
        except DuplicateNicknameException:
            return Response({'message': 'duplicate nickname'}, status=400)
        except DuplicateUserInfoException:
            return Response({'message': 'duplicate user info'}, status=400)

        return Response({"message": "signup successful", "data": response_data}, status=201)


class RefreshTokenView(APIView):
    def post(self, request):
        response_data = refresh_token(request)
        return Response({"message": "token refreshed successful", "data": response_data}, status=200)
