from django.db import models
from django_extensions.db.models import TimeStampedModel

from apps.buyers.models import Buyer
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
    width = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    depth = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    height = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    display_dt = models.DateTimeField(null=True)

    @property
    def thumbnail_image(self):
        return self.item_images.get(is_thumbnail=True)


class ItemImage(TimeStampedModel):
    item_image_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item_images')
    is_thumbnail = models.BooleanField(default=False)
    image = models.FileField(upload_to='items/item_image/', null=False)


class Category(TimeStampedModel):
    category_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=10, null=False, unique=True)


class Color(TimeStampedModel):
    color_id = models.AutoField(primary_key=True)
    color = models.CharField(max_length=10, null=False, unique=True)


class CategoryMapping(TimeStampedModel):
    category_mapping_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='category_mappings')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_mappings')


class ColorMapping(TimeStampedModel):
    color_mapping_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='color_mappings')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='color_mappings')


class Like(TimeStampedModel):
    like_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='likes')
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='likes')


class RecentlyViewedItem(TimeStampedModel):
    recently_viewed_item_id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='recently_viewed_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='recently_viewed_items')
    viewed_date = models.DateTimeField(auto_now_add=True)
    deleted_date = models.DateTimeField()
