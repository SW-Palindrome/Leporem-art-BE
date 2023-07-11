from django.urls import path

from apps.users.views import GoogleAuthUrlView, GoogleLoginView, SignUpView, SignInView

urlpatterns = [
    path('signup/kakao', SignUpView.as_view()),
    path('login/kakao', SignInView.as_view()),
    path('redirect/google', GoogleAuthUrlView.as_view()),
    path('login/google', GoogleLoginView.as_view()),
]
