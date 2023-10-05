from django.urls import path

from apps.deliveries.views import DeliveryInfoTrackingUrlView, RegisterDeliveryInfoView

urlpatterns = [
    path('register', RegisterDeliveryInfoView.as_view()),
    path('orders/<int:order_id>/tracking', DeliveryInfoTrackingUrlView.as_view()),
]
