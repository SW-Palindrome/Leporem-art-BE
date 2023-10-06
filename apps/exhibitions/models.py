from django.db import models
from django_extensions.db.models import TimeStampedModel

from apps.sellers.models import Seller


class Exhibition(TimeStampedModel):
    exhibition_id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(Seller, on_delete=models.PROTECT, related_name='exhibitions')
    title = models.CharField(max_length=46)
    biography = models.CharField(max_length=255)
    cover_image = models.FileField(upload_to='exhibitions/exhibition_cover_image/')
    artist_image = models.FileField(upload_to='exhibitions/exhibition_artist_image/')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    background_color = models.CharField(max_length=10)
    font_family = models.CharField(max_length=50)
    artist_name = models.CharField(max_length=100, default=None)
    is_template = models.BooleanField(default=False)


class ExhibitionItem(TimeStampedModel):
    exhibition_item_id = models.AutoField(primary_key=True)
    exhibition = models.ForeignKey(Exhibition, on_delete=models.CASCADE, related_name='exhibition_items')
    title = models.CharField(max_length=46)
    description = models.CharField(max_length=255)
    template = models.PositiveIntegerField()
    is_sale = models.BooleanField()
    position = models.IntegerField()
    background_color = models.CharField(max_length=10)
    font_family = models.CharField(max_length=50)
    is_custom = models.BooleanField(default=False)


class ExhibitionItemImage(TimeStampedModel):
    exhibition_image_id = models.AutoField(primary_key=True)
    exhibition_item = models.ForeignKey(ExhibitionItem, on_delete=models.CASCADE, related_name='exhibition_images')
    image = models.FileField(upload_to='exhibitions/exhibition_item_image/')


class ExhibitionItemSound(TimeStampedModel):
    exhibition_sound_id = models.AutoField(primary_key=True)
    exhibition_item = models.ForeignKey(ExhibitionItem, on_delete=models.CASCADE, related_name='exhibition_sounds')
    sound = models.FileField(upload_to='exhibitions/exhibition_item_sound/')
