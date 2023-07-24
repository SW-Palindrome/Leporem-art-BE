from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.items.filters import ItemFilter
from apps.items.repositories import ItemRepository
from apps.items.serializers import ItemListSerializer


class LoadItemListView(APIView):
    def get(self, request):
        page_number = request.GET.get('page', 1)
        item_repository = ItemRepository()
        items = item_repository.load_item_list()
        paginator = Paginator(items, 20)

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


class FilterItemView(APIView):
    def get(self, request):
        item_repository = ItemRepository()
        items = item_repository.filter_item()

        page_number = request.GET.get('page', 1)
        ordering = request.GET.get('ordering')
        price = request.GET.get('price')
        category = request.GET.get('category')
        nickname = request.GET.get('nickname')
        search = request.GET.get('search')
        get_params = {
            'ordering': ordering,
            'price': price,
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
