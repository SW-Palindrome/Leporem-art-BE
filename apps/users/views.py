from django.shortcuts import redirect
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.status import HTTP_302_FOUND, HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView

from apps.users.services import GoogleAuthService, KakaoAuthService
from utils.auth.kakao import extract_provider_id

from .open_api_params import get_params


# Create your views here.
class SignUpView(APIView):
    '''회원가입: 이용약관동의여부, 닉네임'''

    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(manual_parameters=get_params)
    def get(self, request):
        # def get(self):
        return Response('Description Test')


    @swagger_auto_schema(responses={201: 'Success'})
    def post(self, request):
        provider_id = extract_provider_id(request.data.get('id_token'))
        is_agree_privacy = request.data.get('is_agree_privacy')
        is_agree_ads = request.data.get('is_agree_ads')
        nickname = request.data.get('nickname')
        kakao_auth_service = KakaoAuthService()
        if kakao_auth_service.signup(provider_id, is_agree_privacy, is_agree_ads, nickname):
            return Response({'message': 'nickname is not valid'}, status=400)

        return Response({'message': 'success'}, status=201)


class GoogleAuthUrlView(APIView):
    """구글 로그인을 위한 URL을 리다이렉팅합니다."""

    @swagger_auto_schema(responses={200: None, HTTP_302_FOUND: openapi.Response('구글 로그인을 위해 리다이렉팅된 URL')})
    def get(self, request):
        google_auth_service = GoogleAuthService()
        return redirect(google_auth_service.get_auth_url())


class GoogleLoginView(APIView):
    def get(self, request):
        google_auth_service = GoogleAuthService()
        user = google_auth_service.login(request.GET['code'])
        if user:
            return Response({'message': 'success'})

        return Response({'message': 'fail'}, status=HTTP_401_UNAUTHORIZED)


class GoogleSignupView(APIView):
    def post(self, request):
        google_auth_service = GoogleAuthService()
        google_auth_service.signup(request.GET['code'])
        return Response({'message': 'success'})
