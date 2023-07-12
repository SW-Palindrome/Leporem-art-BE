from django.conf import settings
from django.urls import path

from apps.users.views import (
    KakaoLogInView,
    KakaoSignUpView,
    RemoveUserView,
    ValidateNicknameView,
)

urlpatterns = [
    path('signup/kakao', KakaoSignUpView.as_view()),
    path('login/kakao', KakaoLogInView.as_view()),
    path('validate/nickname/<str:nickname>', ValidateNicknameView.as_view()),
]

if settings.DEBUG:
    urlpatterns += [
        path('remove', RemoveUserView.as_view()),
    ]
