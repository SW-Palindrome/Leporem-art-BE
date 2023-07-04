from django.shortcuts import redirect
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.status import HTTP_302_FOUND, HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView

from apps.users.services import GoogleAuthService


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
    def get(self, request):
        google_auth_service = GoogleAuthService()
        google_auth_service.signup(request.GET['code'])
        return Response({'message': 'success'})
