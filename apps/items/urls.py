from django.urls import path

from apps.items.views import (
    BuyerItemView,
    FilterItemView,
    LikeItemView,
    SellerItemView,
    ViewedItemView,
)

urlpatterns = [
    path('filter', FilterItemView.as_view()),
    path('detail/buyer', BuyerItemView.as_view()),
    path('like', LikeItemView.as_view()),
    path('detail/seller', SellerItemView.as_view()),
    path('viewed', ViewedItemView.as_view()),
]
