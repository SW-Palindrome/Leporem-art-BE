from django.urls import path

from apps.exhibitions.views import (
    BuyerExhibitionsView,
    ExhibitionArtistView,
    ExhibitionInfoView,
    ExhibitionIntroductionView,
    ExhibitionItemsInfoView,
    ExhibitionItemView,
    ExhibitionView,
    SellerExhibitionsView,
    UploadSoundUrlView,
)

urlpatterns = [
    path('register', ExhibitionView.as_view()),
    path('<int:exhibition_id>/info', ExhibitionInfoView.as_view()),
    path('<int:exhibition_id>/artist-info', ExhibitionArtistView.as_view()),
    path('<int:exhibition_id>/items-info', ExhibitionItemsInfoView.as_view()),
    path('<int:exhibition_id>/introduction', ExhibitionIntroductionView.as_view()),
    path('buyer', BuyerExhibitionsView.as_view()),
    path('seller', SellerExhibitionsView.as_view()),
    path('<int:exhibition_id>/item/<int:exhibition_item_id>', ExhibitionItemView.as_view()),
    path('sound/upload-url', UploadSoundUrlView.as_view()),
]
