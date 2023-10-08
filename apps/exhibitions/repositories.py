from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.utils import timezone

from apps.exhibitions.models import Exhibition
from apps.sellers.models import Seller


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
