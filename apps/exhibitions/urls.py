from django.urls import path

from apps.exhibitions.views import ExhibitionView

urlpatterns = [
    path('register', ExhibitionView.as_view()),
]
