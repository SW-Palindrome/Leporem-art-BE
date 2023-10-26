import random

from rest_framework import permissions
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.exhibitions.repositories import ExhibitionRepository
from apps.exhibitions.serializers import (
    ExhibitionArtistInfoSerializer,
    ExhibitionArtistRegisterSerializer,
    ExhibitionDetailInfoSerializer,
    ExhibitionIntroductionSerializer,
    ExhibitionItemInfoSerializer,
    ExhibitionItemSerializer,
    ExhibitionSerializer,
    ExhibitionsSerializer,
)
from apps.exhibitions.services import ExhibitionItemService, ExhibitionService
from apps.users.permissions import IsExhibitionOwner, IsSeller, IsStaff


class ExhibitionView(APIView):
    permission_classes = [IsStaff]
    serializer_class = ExhibitionSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            ExhibitionRepository().register(
                nickname=serializer.validated_data['nickname'],
                start_date=serializer.validated_data['start_date'],
                end_date=serializer.validated_data['end_date'],
            )
        return Response({'message': 'success'}, status=201)


class ExhibitionIntroductionView(APIView):
    permission_classes = [IsExhibitionOwner]
    serializer_class = ExhibitionIntroductionSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, *args, **kwargs):
        exhibition = ExhibitionRepository().get_introduction(kwargs['exhibition_id'])
        data = self.serializer_class(exhibition).data
        return Response(data, status=200)

    def patch(self, request, exhibition_id):
        self.check_object_permissions(request, self.get_object())
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            ExhibitionRepository().modify_introduction(
                seller_id=request.user.seller.seller_id,
                exhibition_id=exhibition_id,
                cover_image=serializer.validated_data['cover_image'],
                title=serializer.validated_data['title'],
                artist_name=serializer.validated_data['artist_name'],
            )
            return Response({'message': 'success'}, status=200)

    def get_object(self):
        return ExhibitionRepository().get_exhibition(self.kwargs['exhibition_id'])


class ExhibitionArtistView(APIView):
    permission_classes = [AllowAny]
    put_serializer_class = ExhibitionArtistRegisterSerializer
    get_serializer_class = ExhibitionArtistInfoSerializer
    parser_classes = [MultiPartParser]

    def put(self, request, exhibition_id):
        IsExhibitionOwner().has_object_permission(request, self, self.get_object())
        serializer = self.put_serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            ExhibitionService().register_artist_info(
                exhibition_id=exhibition_id,
                is_template=serializer.validated_data['is_template'],
                artist_image=serializer.validated_data.get('artist_image'),
                biography=serializer.validated_data.get('biography'),
                font_family=serializer.validated_data.get('font_family'),
                background_color=serializer.validated_data.get('background_color'),
            )
        return Response({'message': 'success'}, status=200)

    def get(self, request, exhibition_id):
        exhibition = ExhibitionRepository().get_exhibition(exhibition_id)
        data = self.get_serializer_class(exhibition).data
        return Response(data, status=200)

    def get_object(self):
        return ExhibitionRepository().get_exhibition(self.kwargs['exhibition_id'])


class BuyerExhibitionsView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ExhibitionsSerializer

    def get(self, request):
        exhibition_repository = ExhibitionRepository()
        exhibitions = exhibition_repository.get_exhibitions_for_buyer()
        data = self.serializer_class(exhibitions, many=True).data
        random.shuffle(data)
        return Response(data, status=200)


class SellerExhibitionsView(APIView):
    permission_classes = [IsSeller]
    serializer_class = ExhibitionsSerializer

    def get(self, request):
        exhibition_repository = ExhibitionRepository()
        exhibitions = exhibition_repository.get_exhibitions_for_seller(request.user.seller.seller_id)
        data = self.serializer_class(exhibitions, many=True).data
        return Response(data, status=200)


class ExhibitionInfoView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ExhibitionDetailInfoSerializer

    def get(self, request, exhibition_id):
        exhibition_repository = ExhibitionRepository()
        exhibition = exhibition_repository.get_exhibition(exhibition_id)
        data = self.serializer_class(exhibition).data
        return Response(data, status=200)


class ExhibitionItemsInfoView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ExhibitionItemInfoSerializer

    def get(self, request, exhibition_id):
        exhibition_repository = ExhibitionRepository()
        exhibition = exhibition_repository.get_exhibition(exhibition_id)
        data = self.serializer_class(exhibition.exhibition_items, many=True).data
        return Response(data, status=200)


class UploadSoundUrlView(APIView):
    permission_classes = [IsExhibitionOwner]

    def get(self, request):
        extension = request.GET.get('extension', 'mp3')
        return Response(ExhibitionItemService().get_presigned_url_to_post_sound(extension))


class ExhibitionItemView(APIView):
    permission_classes = [IsExhibitionOwner]
    serializer_class = ExhibitionItemSerializer
    parser_classes = [MultiPartParser]

    def post(self, request, exhibition_id):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            ExhibitionItemService().register(
                exhibition_id=exhibition_id,
                seller_id=request.user.seller.seller_id,
                is_custom=serializer.validated_data['is_custom'],
                template=serializer.validated_data.get('template'),
                title=serializer.validated_data.get('title'),
                description=serializer.validated_data.get('description'),
                images=serializer.validated_data['images'],
                sound=serializer.validated_data.get('sound'),
                position=serializer.validated_data['position'],
                background_color=serializer.validated_data.get('background_color'),
                font_family=serializer.validated_data.get('font_family'),
                is_sale=serializer.validated_data['is_sale'],
                shorts_url=serializer.validated_data.get('shorts_url'),
                categories=serializer.validated_data.get('categories', []),
                price=serializer.validated_data.get('price'),
                max_amount=serializer.validated_data.get('max_amount'),
            )
        return Response({'message': 'success'}, status=201)

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            ExhibitionItemService().modify(
                exhibition_id=kwargs['exhibition_id'],
                exhibition_item_id=kwargs['exhibition_item_id'],
                seller_id=request.user.seller.seller_id,
                is_custom=serializer.validated_data['is_custom'],
                template=serializer.validated_data.get('template'),
                title=serializer.validated_data.get('title'),
                description=serializer.validated_data.get('description'),
                images=serializer.validated_data['images'],
                sound=serializer.validated_data.get('sound'),
                position=serializer.validated_data['position'],
                background_color=serializer.validated_data.get('background_color'),
                font_family=serializer.validated_data.get('font_family'),
                is_sale=serializer.validated_data['is_sale'],
                shorts_url=serializer.validated_data.get('shorts_url'),
                price=serializer.validated_data.get('price'),
                current_amount=serializer.validated_data.get('amount'),
            )
            return Response({'message': 'success'}, status=200)
