from django.urls import path

from apps.users.views import GoogleAuthUrlView, GoogleSignupView

urlpatterns = [
    path('login', GoogleAuthUrlView.as_view()),
    path('login/google', GoogleSignupView.as_view()),
]