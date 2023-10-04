from django.urls import path

from apps.deliveries.views import RegisterDeliveryInfoView

urlpatterns = [
    path('register', RegisterDeliveryInfoView.as_view()),
]
