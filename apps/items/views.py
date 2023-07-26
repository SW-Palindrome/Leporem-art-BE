from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.items.filters import ItemFilter
from apps.items.serializers import BuyerDetailedItemSerializer, ItemListSerializer
from apps.items.services import ItemService


class FilterItemView(APIView):
    def get(self, request):
        item_service = ItemService()
        items = item_service.filter_items()

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

            try:
                serializer = ItemListSerializer(page_obj, many=True)

                return Response(
                    {'items': serializer.data},
                    status=200,
                )
            except Exception as e:
                return Response({"error": str(e)}, status=500)
        except PageNotAnInteger:
            return Response({'message': 'PageNotAnInteger'}, status=400)
        except EmptyPage:
            return Response({'message': 'EmptyPage'}, status=400)


class BuyerItemView(APIView):
    def get(self, request):
        item_id = request.GET.get('item_id')
        buyer_id = request.GET.get('buyer_id')

        try:
            item_service = ItemService()
            item = item_service.buyer_detailed_item(item_id, buyer_id)
            try:
                serializer = BuyerDetailedItemSerializer(item, many=True)
                return Response({'item': serializer.data}, status=200)
            except Exception as e:
                return Response({"error": str(e)}, status=400)
        except ObjectDoesNotExist:
            return Response({'message': 'ObjectDoesNotExist'}, status=404)
