from django.urls import path

from apps.sellers.views import (
    SellerItemView,
    SellerMyInfoView,
    SellerRegisterView,
    SellerVerifyView,
)

urlpatterns = [
    path('my', SellerMyInfoView.as_view()),
    path('register', SellerRegisterView.as_view()),
    path('verify', SellerVerifyView.as_view()),
    path('items', SellerItemView.as_view()),
    path('items/<str:item_id>', SellerItemView.as_view()),
]
