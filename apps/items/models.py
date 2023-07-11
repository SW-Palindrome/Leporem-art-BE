from django.core.validators import MaxValueValidator
from django.db import models
from django_extensions.db.models import TimeStampedModel

from apps.sellers.models import Seller


class Item(TimeStampedModel):
    item_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='item')
    price = models.IntegerField(null=True)
    max_amount = models.IntegerField(null=False)
    current_amount = models.IntegerField(null=False)
    title = models.CharField(max_length=46)
    description = models.CharField(max_length=255, null=True)
    shorts = models.IntegerField(validators=[MaxValueValidator(10)], null=False)
    width = models.FloatField(null=False)
    depth = models.FloatField(null=False)
    height = models.FloatField(null=False)


class ItemImage(TimeStampedModel):
    item_image_id = models.AutoField(primary_key=True)
    item = models.OneToOneField(Item, on_delete=models.CASCADE, related_name='item_image')
    is_thumbnail = models.BooleanField(null=False)


class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=10)
    color = models.CharField(max_length=10)

    class Meta:
        constraints = (models.UniqueConstraint(fields=['category', 'color'], name='unique together'),)


class ItemTagMapping(TimeStampedModel):
    item_tag_mapping_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item_tag_mapping')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tag')
