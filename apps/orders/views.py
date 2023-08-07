from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from apps.orders.exceptions import OrderException, ReviewException
from apps.orders.repositories import OrderRepository
from apps.orders.serializers import (
    OrderInfoSerializer,
    OrderSerializer,
    ReviewSerializer,
)
from apps.orders.services import OrderService, ReviewService


class OrderInfoView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderInfoSerializer

    def get(self, request, order_id):
        order_repository = OrderRepository()
        try:
            order = order_repository.get_order(order_id=order_id)
        except OrderException as e:
            return Response({'message': str(e)}, status=HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(order)
        return Response(serializer.data)


class OrderRegisterView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_service = OrderService()
        try:
            order = order_service.order(
                buyer_id=request.user.buyer.buyer_id, item_id=serializer.validated_data['item_id']
            )
        except OrderException as e:
            return Response({'message': str(e)}, status=HTTP_400_BAD_REQUEST)
        return Response({'order_id': order.order_id}, status=HTTP_201_CREATED)


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


class ReviewRegisterView(APIView):
    serializer_class = ReviewSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        review_service = ReviewService()
        try:
            review_service.register(
                order_id=serializer.validated_data['order_id'],
                rating=serializer.validated_data['rating'],
                comment=serializer.validated_data.get('comment'),
            )
        except ReviewException as e:
            return Response({"message": str(e)}, status=400)
        return Response({"message": "success"}, status=201)
