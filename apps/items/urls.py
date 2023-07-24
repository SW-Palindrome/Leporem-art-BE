from django.urls import path

from apps.items.views import FilterItemView, LoadItemListView

urlpatterns = [path('buyers/main', LoadItemListView.as_view()), path('filter', FilterItemView.as_view())]
