from django.urls import path

from apps.exhibitions.views import ExhibitionArtistView, ExhibitionView

urlpatterns = [
    path('register', ExhibitionView.as_view()),
    path('<int:exhibition_id>/artist-info', ExhibitionArtistView.as_view()),
]
