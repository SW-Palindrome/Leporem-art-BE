from django.db import models
from django_extensions.db.models import TimeStampedModel

from apps.sellers.models import Seller


class Item(TimeStampedModel):
    item_id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='items')
    price = models.IntegerField(null=True)
    max_amount = models.IntegerField(null=False)
    current_amount = models.IntegerField(null=False)
    title = models.CharField(max_length=46)
    description = models.CharField(max_length=255, null=True)
    shorts = models.FileField(upload_to='items/item_shorts/', null=False)
    width = models.DecimalField(max_digits=6, decimal_places=2, null=False)
    depth = models.DecimalField(max_digits=6, decimal_places=2, null=False)
    height = models.DecimalField(max_digits=6, decimal_places=2, null=False)
    display_dt = models.DateTimeField(null=True)


class ItemImage(TimeStampedModel):
    item_image_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item_images')
    is_thumbnail = models.BooleanField(default=False)
    image = models.FileField(upload_to='items/item_image/', null=False)


class Tag(TimeStampedModel):
    tag_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=10)
    color = models.CharField(max_length=10)

    class Meta:
        constraints = (models.UniqueConstraint(fields=['category', 'color'], name='unique together'),)


class ItemTagMapping(TimeStampedModel):
    item_tag_mapping_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item_tag_mappings')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='item_tag_mappings')


class Like(TimeStampedModel):
    like_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='likes')
