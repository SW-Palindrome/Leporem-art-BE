from django.urls import path

from apps.sellers.views import SellerItemView, SellerRegisterView, SellerVerifyView

urlpatterns = [
    path('register', SellerRegisterView.as_view()),
    path('verify', SellerVerifyView.as_view()),
    path('items', SellerItemView.as_view()),
]
