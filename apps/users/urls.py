from django.conf import settings
from django.urls import path

from apps.users.views import (
    GoogleAuthUrlView,
    GoogleLoginView,
    RemoveUserView,
    SignInView,
    SignUpView,
)

urlpatterns = [
    path('signup/kakao', SignUpView.as_view()),
    path('login/kakao', SignInView.as_view()),
    path('redirect/google', GoogleAuthUrlView.as_view()),
    path('login/google', GoogleLoginView.as_view()),
]

if settings.DEBUG:
    urlpatterns += [
        path('remove', RemoveUserView.as_view()),
    ]
