from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from apps.orders.exceptions import OrderException
from apps.orders.serializers import OrderSerializer
from apps.orders.services import OrderService


class OrderRegisterView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_service = OrderService()
        try:
            order_service.order(buyer_id=request.user.buyer.buyer_id, item_id=serializer.validated_data['item_id'])
        except OrderException as e:
            return Response({'message': str(e)}, status=HTTP_400_BAD_REQUEST)
        return Response(status=HTTP_201_CREATED)


class OrderDeliveryStartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        order_service = OrderService()
        try:
            order_service.start_delivery(request.user.seller.seller_id, order_id)
        except OrderException as e:
            return Response({'message': str(e)}, status=HTTP_400_BAD_REQUEST)
        return Response(status=HTTP_201_CREATED)


class OrderDeliveryCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        order_service = OrderService()
        try:
            order_service.complete_delivery(request.user.seller.seller_id, order_id)
        except OrderException as e:
            return Response({'message': str(e)}, status=HTTP_400_BAD_REQUEST)
        return Response(status=HTTP_201_CREATED)


class OrderCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        order_service = OrderService()
        try:
            order_service.cancel(request.user.buyer.buyer_id, order_id)
        except OrderException as e:
            return Response({'message': str(e)}, status=HTTP_400_BAD_REQUEST)
        return Response(status=HTTP_201_CREATED)
