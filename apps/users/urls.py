from django.urls import path

from apps.users.views import GoogleAuthUrlView, GoogleLoginView, GoogleSignupView

urlpatterns = [
    path('redirect/google', GoogleAuthUrlView.as_view()),
    path('login/google', GoogleLoginView.as_view()),
    path('signup/google', GoogleSignupView.as_view()),
]
