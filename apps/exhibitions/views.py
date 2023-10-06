from rest_framework.response import Response
from rest_framework.views import APIView

from apps.exhibitions.repositories import ExhibitionRepository
from apps.exhibitions.serializers import ExhibitionSerializer
from apps.users.permissions import IsStaff


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
