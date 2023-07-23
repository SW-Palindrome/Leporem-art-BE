from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

from apps.orders.repositories import OrderRepository
from apps.orders.serializers import OrderSerializer


class OrderRegisterView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_repository = OrderRepository()
        order_repository.order(buyer_id=request.user.buyer.buyer_id, item_id=serializer.validated_data['item_id'])
        return Response(status=HTTP_201_CREATED)
