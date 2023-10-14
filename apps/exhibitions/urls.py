from django.urls import path

from apps.exhibitions.views import (
    BuyerExhibitionsView,
    ExhibitionArtistView,
    ExhibitionDetailView,
    ExhibitionIntroductionView,
    ExhibitionView,
    SellerExhibitionsView,
)

urlpatterns = [
    path('register', ExhibitionView.as_view()),
    path('<int:exhibition_id>/artist-info', ExhibitionArtistView.as_view()),
    path('introduction/<int:exhibition_id>', ExhibitionIntroductionView.as_view()),
    path('buyer', BuyerExhibitionsView.as_view()),
    path('seller', SellerExhibitionsView.as_view()),
    path('<int:exhibition_id>', ExhibitionDetailView.as_view()),
]
