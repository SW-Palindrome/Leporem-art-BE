from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.buyers.serializers import BuyerInfoSerializer
from apps.users.repositories import UserRepository


class BuyerMyInfoView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BuyerInfoSerializer

    def get(self, request):
        user = UserRepository().get_user_info(request.user.user_id)
        data = self.serializer_class(user).data
        return Response(data, status=200)
