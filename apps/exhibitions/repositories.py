from django.db import transaction

from apps.exhibitions.models import Exhibition
from apps.sellers.models import Seller
from utils.files import create_random_filename


class ExhibitionRepository:
    @transaction.atomic
    def register(self, nickname, start_date, end_date):
        seller = Seller.objects.get(user__nickname=nickname)
        exhibition = Exhibition.objects.create(
            seller=seller,
            start_date=start_date,
            end_date=end_date,
            artist_name=seller.user.nickname,
        )
        return exhibition

    def register_artist_info(self, exhibition_id, biography, artist_image):
        exhibition = Exhibition.objects.get(exhibition_id=exhibition_id)
        exhibition.biography = biography
        artist_image.name = create_random_filename(artist_image.name)
        exhibition.artist_image = artist_image
        exhibition.save()
        return exhibition
