from django.urls import path

from apps.buyers.views import BuyerMyInfoView

urlpatterns = [
    path('my', BuyerMyInfoView.as_view()),
]
