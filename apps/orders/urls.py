from django.urls import path

from apps.orders.views import OrderView

urlpatterns = [
    path('', OrderView.as_view()),
]
