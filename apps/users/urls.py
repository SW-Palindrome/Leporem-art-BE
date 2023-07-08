from django.urls import path

from apps.users.views import (
    ConsentPrivacyView,
    GoogleAuthUrlView,
    GoogleLoginView,
    GoogleSignupView,
    KakaoSigninView,
    KakaoSignupView,
)

urlpatterns = [
    path('consent-privacy/', ConsentPrivacyView.as_view()),
    path('redirect/google', GoogleAuthUrlView.as_view()),
    path('login/google', GoogleLoginView.as_view()),
    path('signup/google', GoogleSignupView.as_view()),
    path('login/kakao', KakaoSigninView.as_view()),
    path('signup/kakao', KakaoSignupView.as_view()),
]
