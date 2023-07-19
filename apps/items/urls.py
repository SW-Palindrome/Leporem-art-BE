from django.urls import path

from apps.items.views import LoadItemListView

urlpatterns = [
    path('buyers/main', LoadItemListView.as_view()),
]
