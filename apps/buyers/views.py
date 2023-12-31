from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.buyers.serializers import BuyerInfoSerializer, BuyerMyOrderSerializer
from apps.orders.repositories import OrderRepository
from apps.users.repositories import UserRepository


class BuyerMyInfoView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BuyerInfoSerializer

    def get(self, request):
        user = UserRepository().get_user_info(request.user.user_id)
        data = self.serializer_class(user).data
        return Response(data, status=200)


class BuyerMyOrderView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BuyerMyOrderSerializer

    def get(self, request):
        order_repository = OrderRepository()
        orders = order_repository.get_order_list_by_buyer(self.request.user.buyer.buyer_id)
        data = self.serializer_class(orders, many=True).data
        return Response(data, status=200)
