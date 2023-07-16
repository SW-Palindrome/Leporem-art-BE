from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.items.services import LoadItemListService


class LoadItemListView(APIView):
    def get(self, request):
        load_item_list_service = LoadItemListService()
        page_number = request.GET.get('page')
        try:
            nicknames = load_item_list_service.load_nickname()
            items = load_item_list_service.load_item()
            images = load_item_list_service.load_image()
            likes = load_item_list_service.load_likes()
            try:
                paginator_nicknames = Paginator(nicknames, 20)
                paginator_items = Paginator(items, 20)
                paginator_images = Paginator(images, 20)
                paginator_likes = Paginator(likes, 20)
                page_nicknames = paginator_nicknames.get_page(page_number)
                page_items = paginator_items.get_page(page_number)
                page_images = paginator_images.get_page(page_number)
                page_likes = paginator_likes.get_page(page_number)

                return Response(
                    [{'nicknames': page_nicknames, 'items': page_items, 'images': page_images, 'likes': page_likes}],
                    status=200,
                )
            except PageNotAnInteger:
                return Response({'message': 'PageNotAnInteger'}, status=400)
            except EmptyPage:
                return Response({'message': 'EmptyPage'}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
