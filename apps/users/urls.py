from django.urls import path

from apps.users.views import (
    AppleCallBackView,
    AppleLoginUrlView,
    AppleSignUpView,
    ChangeNicknameView,
    ChangeProfileImageView,
    KakaoLogInView,
    KakaoSignUpView,
    MyInfoView,
    RefreshTokenView,
    ValidateNicknameView,
)

urlpatterns = [
    path('signup/kakao', KakaoSignUpView.as_view()),
    path('login/kakao', KakaoLogInView.as_view()),
    path('validate/nickname/<str:nickname>', ValidateNicknameView.as_view()),
    path('nickname', ChangeNicknameView.as_view()),
    path('profile-image', ChangeProfileImageView.as_view()),
    path('redirect/apple', AppleLoginUrlView.as_view()),
    path('login/apple', AppleCallBackView.as_view()),
    path('signup/apple', AppleSignUpView.as_view()),
    path('refresh', RefreshTokenView.as_view()),
    path('info/my', MyInfoView.as_view()),
]
