import re

from django.shortcuts import redirect
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.status import HTTP_302_FOUND, HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView

from apps.users.services import GoogleAuthService, KakaoAuthService

from .open_api_params import get_params, get_params2
from .serializers import ConsentSerializer


# Create your views here.
class ConsentPrivacyView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(manual_parameters=get_params)
    def get(self, request):
        return Response('Description Test')

    @swagger_auto_schema(request_body=ConsentSerializer, responses={201: 'Success'})
    def post(self):
        consents = ConsentSerializer(data=request.data)
        if consents.is_valid():
            consents.save()
            return Response(consents.data)
        return Response(consents.errors, status=400)


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


'''KAKAO'''


class KakaoSignupView(APIView):
    @swagger_auto_schema(manual_parameters=get_params2)
    def post(self, request):
        # nickname='abc'
        nickname_pattern = r'^[A-Za-z0-9가-힣_-]+$'
        if not re.match(nickname_pattern, request.GET['nickname']):
            return Response({'error': 'Invalid nickname'}, status=400)
        kakao_auth_service = KakaoAuthService()
        kakao_auth_service.signup(request.GET['provider_id'], request.GET['nickname'])
        return Response({'message': 'success'}, status=201)


class KakaoSigninView(APIView):
    """Kakao User Signin"""

    @swagger_auto_schema()
    def get(self, request):
        temp_signature = ''
        kakao_auth_service = KakaoAuthService()
        user = kakao_auth_service.signin(
            temp_signature,
            request.GET['provider_id'],
            #'1234'
        )
        if user:
            return Response({'message': 'success'})

        return Response({'message': 'failed'}, status=401)
