from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.utils import timezone

from apps.exhibitions.models import (
    Exhibition,
    ExhibitionItem,
    ExhibitionItemImage,
    ExhibitionItemSound,
)
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

    @transaction.atomic
    def modify_introduction(self, seller_id, exhibition_id, cover_image, title, artist_name):
        try:
            exhibition = Seller.objects.get(seller_id=seller_id).exhibitions.get(exhibition_id=exhibition_id)
        except Exhibition.DoesNotExist:
            raise PermissionDenied

        cover_image.name = create_random_filename(cover_image.name)
        exhibition.cover_image = cover_image
        exhibition.title = title
        exhibition.artist_name = artist_name
        exhibition.save()

        return exhibition

    def get_introduction(self, exhibition_id):
        return Exhibition.objects.get(exhibition_id=exhibition_id)

    def get_exhibitions_for_buyer(self):
        today = timezone.now().date()
        return Exhibition.objects.filter(
            start_date__lte=today,
            end_date__gte=today,
        )

    def get_exhibitions_for_seller(self, seller_id):
        seller = Seller.objects.get(seller_id=seller_id)
        return Exhibition.objects.filter(seller=seller).order_by('-start_date')

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

    def get_exhibition(self, exhibition_id):
        return Exhibition.objects.get(exhibition_id=exhibition_id)


class ExhibitionItemRepository:
    @transaction.atomic
    def register(
        self,
        exhibition_id,
        item,
        is_custom,
        template,
        title,
        description,
        images,
        sound,
        position,
        background_color,
        font_family,
        is_sale,
    ):
        if template and (template < 1 or template > 9):
            raise ValueError('template 번호는 1~9 사이의 값이어야 합니다.')

        exhibition = Exhibition.objects.get(exhibition_id=exhibition_id)
        exhibition_item = ExhibitionItem.objects.create(
            exhibition=exhibition,
            item=item,
            is_custom=is_custom,
            template=template,
            title=title,
            description=description,
            position=position,
            background_color=background_color,
            font_family=font_family,
            is_sale=is_sale,
        )
        for image in images:
            ExhibitionItemImage.objects.create(
                exhibition_item=exhibition_item,
                image=image,
            )
        ExhibitionItemSound.objects.create(
            exhibition_item=exhibition_item,
            sound=sound,
        )
        return exhibition_item
