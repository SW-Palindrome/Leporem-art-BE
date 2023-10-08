from django.urls import path

from apps.sellers.views import (
    SellerControlAmountView,
    SellerDescriptionView,
    SellerExhibitionIntroductionView,
    SellerInfoView,
    SellerItemView,
    SellerMyInfoView,
    SellerMyOrderView,
    SellerRegisterView,
    SellerUploadShortsUrlView,
    SellerVerifyView,
)

urlpatterns = [
    path('register', SellerRegisterView.as_view()),
    path('verify', SellerVerifyView.as_view()),
    path('descriptions', SellerDescriptionView.as_view()),
    path('items', SellerItemView.as_view()),
    path('items/<str:item_id>', SellerItemView.as_view()),
    path('info', SellerMyInfoView.as_view()),
    path('info/<str:nickname>', SellerInfoView.as_view()),
    path('orders/my', SellerMyOrderView.as_view()),
    path('current-amount', SellerControlAmountView.as_view()),
    path('shorts/upload-url', SellerUploadShortsUrlView.as_view()),
    path('exhibition-intro/<str:exhibition_id>', SellerExhibitionIntroductionView.as_view()),
]
