from django.urls import path

from apps.buyers.views import BuyerExhibitionsView, BuyerMyInfoView, BuyerMyOrderView

urlpatterns = [
    path('info', BuyerMyInfoView.as_view()),
    path('orders/my', BuyerMyOrderView.as_view()),
    path('exhibitions', BuyerExhibitionsView.as_view()),
]
