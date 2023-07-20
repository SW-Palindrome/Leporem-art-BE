from django.conf import settings
from django.urls import path

from apps.users.views import (
    ChangeNicknameView,
    ChangeProfileImageView,
    KakaoLogInView,
    KakaoSignUpView,
    RemoveUserView,
    UserView,
    ValidateNicknameView,
)

urlpatterns = [
    path('', UserView.as_view()),
    path('signup/kakao', KakaoSignUpView.as_view()),
    path('login/kakao', KakaoLogInView.as_view()),
    path('validate/nickname/<str:nickname>', ValidateNicknameView.as_view()),
    path('nickname', ChangeNicknameView.as_view()),
    path('profile-image', ChangeProfileImageView.as_view()),
]

if settings.DEBUG:
    urlpatterns += [
        path('remove', RemoveUserView.as_view()),
    ]
