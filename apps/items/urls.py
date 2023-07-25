from django.urls import path

from apps.items.views import FilterItemView

urlpatterns = [path('filter', FilterItemView.as_view())]
