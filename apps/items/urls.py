from django.urls import path

from apps.items.views import BuyerItemView, FilterItemView

urlpatterns = [
    path('filter', FilterItemView.as_view()),
    path('buyer/detail', BuyerItemView.as_view()),
]
