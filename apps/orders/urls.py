from django.urls import path

from apps.orders.views import (
    OrderCancelView,
    OrderDeliveryCompleteView,
    OrderDeliveryStartView,
    OrderInfoView,
    OrderRegisterView,
    ReviewRegisterView,
)

urlpatterns = [
    path('register', OrderRegisterView.as_view()),
    path('<int:order_id>', OrderInfoView.as_view()),
    path('<int:order_id>/delivery-start', OrderDeliveryStartView.as_view()),
    path('<int:order_id>/delivery-complete', OrderDeliveryCompleteView.as_view()),
    path('<int:order_id>/cancel', OrderCancelView.as_view()),
    path('review', ReviewRegisterView.as_view()),
]
