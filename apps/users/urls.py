from django.conf import settings
from django.urls import path

from apps.users.views import (
    KakaoLogInView,
    RemoveUserView,
    KakaoSignUpView,
)

urlpatterns = [
    path('signup/kakao', KakaoSignUpView.as_view()),
    path('login/kakao', KakaoLogInView.as_view()),
]

if settings.DEBUG:
    urlpatterns += [
        path('remove', RemoveUserView.as_view()),
    ]
