from django.db import models
from django_extensions.db.models import TimeStampedModel

from apps.sellers.models import Seller


class Exhibition(TimeStampedModel):
    exhibition_id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(Seller, on_delete=models.PROTECT)
    title = models.CharField(max_length=46)
    biography = models.CharField(max_length=255)
    image = models.FileField(upload_to='exhibitions/exhibition_cover_image/')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    color = models.CharField(max_length=10)
    font = models.CharField(max_length=50)
