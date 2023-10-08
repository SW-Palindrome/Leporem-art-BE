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

    def get_exhibitions_for_buyer(self):
        today = timezone.now().date()
        return Exhibition.objects.filter(
            start_date__lte=today,
            end_date__gte=today,
        )
