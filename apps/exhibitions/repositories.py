from django.utils import timezone

from apps.exhibitions.models import Exhibition


class ExhibitionRepository:
    def get_exhibitions(self):
        today = timezone.now().date()
        return Exhibition.objects.filter(
            start_date__lte=today,
            end_date__gte=today,
        )
