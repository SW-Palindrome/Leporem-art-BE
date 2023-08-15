from django.conf import settings
from django.shortcuts import redirect
from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.repositories import UserRepository
from apps.users.services import AuthService, UserService
from utils.auth.apple import AppleOAuth2
from utils.auth.kakao import extract_provider_id, validate_id_token
from utils.auth.leporemart import generate_access_token, refresh_token

from .exceptions import DuplicateNicknameException, DuplicateUserInfoException
from .permissions import IsStaff
from .serializers import ChangeNicknameSerializer, ChangeProfileImageSerializer


# Create your views here.
class KakaoSignUpView(APIView):
    """회원가입: 이용약관동의여부, 닉네임"""

    PROVIDER = 'KAKAO'
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        id_token = request.data.get('id_token')
        if not validate_id_token(id_token):
            return Response({'message': 'invalid id_token'}, status=400)

        provider_id = extract_provider_id(id_token)
        is_agree_privacy = request.data.get('is_agree_privacy')
        is_agree_terms = request.data.get('is_agree_terms')
        is_agree_ads = request.data.get('is_agree_ads')
        nickname = request.data.get('nickname')
        auth_service = AuthService()

        access_token, access_exp = generate_access_token(self.PROVIDER, extract_provider_id(id_token), "access")
        user_refresh_token, refresh_exp = generate_access_token(self.PROVIDER, extract_provider_id(id_token), "refresh")

        response_data = {
            'access_token': access_token,
            'refresh_token': user_refresh_token,
            'access_exp': access_exp,
        }

        try:
            auth_service.signup(
                provider=self.PROVIDER,
                provider_id=provider_id,
                refresh_token=user_refresh_token,
                is_agree_privacy=is_agree_privacy,
                is_agree_terms=is_agree_terms,
                is_agree_ads=is_agree_ads,
                nickname=nickname,
            )
        except DuplicateNicknameException:
            return Response({'message': 'duplicate nickname'}, status=400)
        except DuplicateUserInfoException:
            return Response({'message': 'duplicate user info'}, status=400)

        return Response({'message': 'success', 'data': response_data}, status=201)


class KakaoLogInView(APIView):
    """로그인: 최초회원가입 이후 재로그인"""

    PROVIDER = 'KAKAO'
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        auth_service = AuthService()
        id_token = request.data.get('id_token')

        try:
            user = auth_service.login(id_token=request.data.get('id_token'))
        except AuthenticationFailed as e:
            return Response({'message': str(e)}, status=403)
        if user is None:
            return Response({'message': 'signin failed'}, status=403)

        access_token, access_exp = generate_access_token(self.PROVIDER, extract_provider_id(id_token), "access")
        user_refresh_token, refresh_exp = generate_access_token(self.PROVIDER, extract_provider_id(id_token), "refresh")

        UserRepository().refresh_token(user.user_id, user_refresh_token)

        return Response(
            {
                'user_id': user.user_id,
                'is_seller': user.is_seller,
                'nickname': user.nickname,
                'access_token': access_token,
                'refresh_token': user_refresh_token,
                'access_exp': access_exp,
            },
            status=200,
        )


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
        redirect_uri = 'https://dev.leporem.art/users/login/apple'
        uri = f"{self.APPLE_AUTH_URL}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}"

        res = redirect(uri)
        return res


class AppleCallBackView(APIView):
    permission_classes = [permissions.AllowAny]

    PROVIDER = "APPLE"

    def get(self, request):
        data = request.query_params
        code = data.get('code')

        apple_oauth = AppleOAuth2()
        user_details = apple_oauth.do_auth(code)

        user_repository = UserRepository()
        user = user_repository.login(self.PROVIDER, user_details.get('sub'))

        if user:
            access_token, access_exp = generate_access_token(self.PROVIDER, user_details['sub'], "access")
            refresh_token, refresh_exp = generate_access_token(self.PROVIDER, user_details['sub'], "refresh")
            user_repository.refresh_token(user.user_id, refresh_token)

            response_data = {
                'user_id': user.user_id,
                'is_seller': user.is_seller,
                'nickname': user.nickname,
                'access_token': access_token,
                'refresh_token': refresh_token,
                'access_exp': access_exp,
            }
            return Response({"message": "success", "data": response_data}, status=200)
        return Response({"message": "signup required", "user_data": user_details['sub']}, status=404)


class AppleSignUpView(APIView):
    permission_classes = [permissions.AllowAny]

    PROVIDER = "APPLE"

    def post(self, request):
        """자체 token, refresh token 생성 필요"""
        user_data = request.data.get('user_data')
        is_agree_privacy = request.data.get('is_agree_privacy')
        is_agree_terms = request.data.get('is_agree_terms')
        is_agree_ads = request.data.get('is_agree_ads')
        nickname = request.data.get('nickname')

        auth_service = AuthService()

        access_token, access_exp = generate_access_token(self.PROVIDER, user_data, "access")
        refresh_token, refresh_exp = generate_access_token(self.PROVIDER, user_data, "refresh")

        response_data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'access_exp': access_exp,
        }

        try:
            auth_service.signup(
                self.PROVIDER, user_data, refresh_token, is_agree_privacy, is_agree_terms, is_agree_ads, nickname
            )
        except DuplicateNicknameException:
            return Response({'message': 'duplicate nickname'}, status=400)
        except DuplicateUserInfoException:
            return Response({'message': 'duplicate user info'}, status=400)

        return Response({"message": "signup successful", "data": response_data}, status=201)


class RefreshTokenView(APIView):
    def post(self, request):
        response_data = refresh_token(request)
        return Response({"message": "token refreshed successful", "data": response_data}, status=200)
