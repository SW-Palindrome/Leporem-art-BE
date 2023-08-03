from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.items.exceptions import ViewedException
from apps.items.filters import ItemFilter
from apps.items.serializers import (
    BuyerDetailedItemSerializer,
    BuyerItemListSerializer,
    FavoriteItemListSerializer,
    SellerDetailedItemSerializer,
    SellerTotalItemSerializer,
    ViewedItemListSerializer,
)
from apps.items.services import ItemService, LikeService, ViewedItemService


class FilterItemView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        buyer_id = request.user.buyer.buyer_id

        item_service = ItemService()
        items = item_service.filter_items(buyer_id)

        page_number = request.GET.get('page', 1)
        ordering = request.GET.get('ordering')
        category = request.GET.get('category')
        nickname = request.GET.get('nickname')
        search = request.GET.get('search')
        price = request.GET.get('price')

        if price:
            price_min, price_max = price.split(',')
        else:
            price_min, price_max = None, None

        get_params = {
            'ordering': ordering,
            'price_min': price_min,
            'price_max': price_max,
            'category': category,
            'nickname': nickname,
            'search': search,
        }

        filtered_items = ItemFilter(get_params, queryset=items)

        paginator = Paginator(filtered_items.qs, 20)

        try:
            page_number = int(page_number)
            page_obj = paginator.page(page_number)

            if nickname:
                seller_serializer = SellerTotalItemSerializer(page_obj, context={'items': page_obj})
                return Response({"list": seller_serializer.data}, status=200)
            buyer_serializer = BuyerItemListSerializer(page_obj, many=True)
            return Response({"items": buyer_serializer.data}, status=200)
        except PageNotAnInteger:
            return Response({"message": "PageNotAnInteger"}, status=400)
        except EmptyPage:
            return Response({"message": "EmptyPage"}, status=400)


class BuyerItemView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        item_id = request.GET.get('item_id')
        buyer_id = request.user.buyer.buyer_id

        item_service = ItemService()
        item = item_service.buyer_detailed_item(item_id, buyer_id)
        if item:
            try:
                serializer = BuyerDetailedItemSerializer(item)
                return Response({"detail": serializer.data}, status=200)
            except Exception as e:
                return Response({"error": str(e)}, status=400)
        return Response({"message": "ObjectDoesNotExist"}, status=404)


class LikeItemView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        item_id = request.GET.get('item_id')
        buyer_id = request.user.buyer.buyer_id
        like_service = LikeService()
        if like_service.check_like(item_id, buyer_id):
            return Response({"message": "success"}, status=200)
        return Response({"message": "ObjectDoesNotExist"}, status=404)

    def post(self, request):
        item_id = request.data.get('item_id')
        buyer_id = request.user.buyer.buyer_id
        like_service = LikeService()
        if like_service.on_like(item_id, buyer_id):
            return Response({"message": "success"}, status=200)
        return Response({"message": "set like failed"}, status=400)

    def delete(self, request):
        item_id = request.data.get('item_id')
        buyer_id = request.user.buyer.buyer_id
        like_service = LikeService()
        if like_service.off_like(item_id, buyer_id):
            return Response({"message": "success"}, status=200)
        return Response({"message": "remove like failed"}, status=400)


class SellerItemView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        item_id = request.GET.get('item_id')
        seller_id = request.user.seller.seller_id

        item_service = ItemService()
        item = item_service.seller_detailed_item(item_id, seller_id)
        if item:
            reviews = item_service.detailed_item_review(item_id)
            try:
                serializer = SellerDetailedItemSerializer(item, many=True, context={'reviews': reviews})
                return Response({"detail": serializer.data}, status=200)
            except Exception as e:
                return Response({"error": str(e)}, status=400)
        return Response({"message": "ObjectDoesNotExist"}, status=404)


class ViewedItemView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        buyer = request.user.buyer.buyer_id
        viewed_item_service = ViewedItemService()
        try:
            viewed_items = viewed_item_service.viewed_items(buyer)
            try:
                serializer = ViewedItemListSerializer(viewed_items, many=True)
                return Response({"items": serializer.data}, status=200)
            except Exception as e:
                return Response({"error": str(e)}, status=400)
        except ViewedException as e:
            return Response({"error": str(e)}, status=404)

    def post(self, request):
        item = request.data.get('item_id')
        buyer = request.user.buyer.buyer_id
        viewed_item_service = ViewedItemService()
        try:
            viewed_item_service.add_viewed_item(item, buyer)
            return Response({"message": "success"}, status=201)
        except ViewedException as e:
            return Response({"error": str(e)}, status=404)

    def delete(self, request):
        item = request.data.get('item_id')
        buyer = request.user.buyer.buyer_id
        viewed_item_service = ViewedItemService()

        try:
            viewed_item_service.delete_viewed_item(item, buyer)
            return Response({"message": "success"}, status=200)
        except ViewedException as e:
            return Response({"error": str(e)}, status=404)


class FavoriteItemView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        buyer = request.user.buyer.buyer_id
        item_service = ItemService()

        try:
            favorite_items = item_service.favorite_items(buyer)
            if favorite_items:
                serializer = FavoriteItemListSerializer(favorite_items, many=True)
                return Response({"items": serializer.data}, status=200)
            return Response({"There are no recently viewed items."}, status=404)
        except ViewedException as e:
            return Response({"error": str(e)}, status=400)
