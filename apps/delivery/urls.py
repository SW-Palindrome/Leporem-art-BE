from django.urls import path

from apps.delivery.views import RegisterDeliveryInfoView

urlpatterns = [
    path('register', RegisterDeliveryInfoView.as_view()),
]
