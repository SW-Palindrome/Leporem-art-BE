from django.urls import path

from apps.orders.views import OrderRegisterView

urlpatterns = [
    path('register', OrderRegisterView.as_view()),
]
