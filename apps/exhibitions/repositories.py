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

    def register_artist_info(self, exhibition_id, biography, artist_image, font_family, background_color):
        exhibition = Exhibition.objects.get(exhibition_id=exhibition_id)
        exhibition.biography = biography
        artist_image.name = create_random_filename(artist_image.name)
        exhibition.artist_image = artist_image
        exhibition.font_family = font_family
        exhibition.background_color = background_color
        exhibition.is_template = True
        exhibition.save()
        return exhibition

    def register_custom_artist_info(self, exhibition_id, artist_image):
        exhibition = Exhibition.objects.get(exhibition_id=exhibition_id)
        artist_image.name = create_random_filename(artist_image.name)
        exhibition.artist_image = artist_image
        exhibition.biography = ''
        exhibition.font_family = ''
        exhibition.background_color = ''
        exhibition.is_template = False
        exhibition.save()
        return exhibition
