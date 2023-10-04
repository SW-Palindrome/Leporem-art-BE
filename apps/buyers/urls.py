from django.urls import path

from apps.buyers.views import BuyerExhibitionView, BuyerMyInfoView, BuyerMyOrderView

urlpatterns = [
    path('info', BuyerMyInfoView.as_view()),
    path('orders/my', BuyerMyOrderView.as_view()),
    path('exhibitions', BuyerExhibitionView.as_view()),
]
