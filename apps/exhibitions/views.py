from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.exhibitions.repositories import ExhibitionRepository
from apps.exhibitions.serializers import (
    ExhibitionArtistRegisterSerializer,
    ExhibitionSerializer,
)
from apps.exhibitions.services import ExhibitionService
from apps.users.permissions import IsExhibitionOwner, IsStaff


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


class ExhibitionArtistView(APIView):
    permission_classes = [IsExhibitionOwner]
    serializer_class = ExhibitionArtistRegisterSerializer
    parser_classes = [MultiPartParser]

    def post(self, request, exhibition_id):
        self.check_object_permissions(request, self.get_object())
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            ExhibitionService().register_artist_info(
                exhibition_id=exhibition_id,
                is_template=serializer.validated_data['is_template'],
                artist_image=serializer.validated_data.get('artist_image'),
                biography=serializer.validated_data.get('biography'),
                font_family=serializer.validated_data.get('font_family'),
                background_color=serializer.validated_data.get('background_color'),
            )
        return Response({'message': 'success'}, status=201)

    def get_object(self):
        return ExhibitionRepository().get_exhibition(self.kwargs['exhibition_id'])
