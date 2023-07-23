from django.urls import path

from apps.buyers.views import BuyerMyInfoView

urlpatterns = [
    path('info', BuyerMyInfoView.as_view()),
]
