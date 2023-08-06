from django.conf import settings
from django.urls import path

from apps.users.views import (
    AppleLoginUrlView,
    AppleLoginView,
    AppleSignUpView,
    ChangeNicknameView,
    ChangeProfileImageView,
    KakaoLogInView,
    KakaoSignUpView,
    RefreshTokenView,
    RemoveUserView,
    ValidateNicknameView,
)

urlpatterns = [
    path('signup/kakao', KakaoSignUpView.as_view()),
    path('login/kakao', KakaoLogInView.as_view()),
    path('validate/nickname/<str:nickname>', ValidateNicknameView.as_view()),
    path('nickname', ChangeNicknameView.as_view()),
    path('profile-image', ChangeProfileImageView.as_view()),
    path('login/apple', AppleLoginUrlView.as_view()),
    path('validate/apple', AppleLoginView.as_view()),
    path('signup/apple', AppleSignUpView.as_view()),
    path('refresh', RefreshTokenView.as_view()),
]

if settings.DEBUG:
    urlpatterns += [
        path('remove', RemoveUserView.as_view()),
    ]
