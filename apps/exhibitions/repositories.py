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
            status=Exhibition.Status.CREATED,
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

        if exhibition.status == Exhibition.Status.CREATED.value:
            exhibition.status = Exhibition.Status.INTRODUCTION_WRITTEN.value

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

        if exhibition.status == Exhibition.Status.INTRODUCTION_WRITTEN.value:
            exhibition.status = Exhibition.Status.ARTIST_WRITTEN.value

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

    @transaction.atomic
    def modify(
        self,
        exhibition_id,
        exhibition_item_id,
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
        try:
            exhibition_item = Exhibition.objects.get(exhibition_id=exhibition_id).exhibition_items.get(
                exhibition_item_id=exhibition_item_id
            )
        except ExhibitionItem.DoesNotExist:
            raise PermissionDenied

        exhibition_item.is_custom = is_custom
        exhibition_item.template = template
        exhibition_item.title = title
        exhibition_item.description = description
        exhibition_item.position = position
        exhibition_item.background_color = background_color
        exhibition_item.font_family = font_family
        exhibition_item.is_sale = is_sale
        exhibition_item.save()

        exhibition_item.exhibition_images.all().delete()
        exhibition_item.exhibition_sounds.all().delete()

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

    @transaction.atomic
    def delete(self, exhibition_item_id):
        exhibition_item = ExhibitionItem.objects.get(exhibition_item_id=exhibition_item_id)
        exhibition_item.exhibition_images.all().delete()
        exhibition_item.exhibition_sounds.all().delete()
        if exhibition_item.is_sale:
            exhibition_item.item.delete()
        exhibition_item.delete()

    def get_exhibition_item(self, exhibition_item_id):
        return ExhibitionItem.objects.get(exhibition_item_id=exhibition_item_id)
