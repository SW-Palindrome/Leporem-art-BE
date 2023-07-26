from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.orders.repositories import OrderRepository
from apps.sellers.filters import SellerMyOrderFilterBackend
from apps.sellers.repositories import SellerRepository
from apps.sellers.serializers import (
    DescriptionSerializer,
    SellerInfoSerializer,
    SellerItemSerializer,
    SellerMyInfoSerializer,
    SellerMyOrderSerializer,
    SellerRegisterSerializer,
    SellerVerifySerializer,
)
from apps.sellers.services import SellerRegisterService, SellerService
from apps.users.permissions import IsBuyerOnly, IsSeller


class SellerRegisterView(APIView):
    permission_classes = [IsBuyerOnly]
    serializer_class = SellerRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            SellerRegisterService().send_verify_email(
                user=request.user,
                email=serializer.validated_data['email'],
            )
        return Response({'message': 'success'})


class SellerVerifyView(APIView):
    permission_classes = [IsBuyerOnly]
    serializer_class = SellerVerifySerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            seller = SellerRegisterService().verify(
                user=request.user,
                verify_code=serializer.validated_data['verify_code'],
            )
            if seller:
                return Response({'message': 'success'})
        return Response({'message': 'fail'})


class SellerItemView(APIView):
    permission_classes = [IsSeller]
    parser_classes = [MultiPartParser]
    serializer_class = SellerItemSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            seller_service = SellerService()
            seller_service.register_item(
                seller_id=request.user.seller.seller_id,
                price=serializer.validated_data['price'],
                max_amount=serializer.validated_data['max_amount'],
                title=serializer.validated_data['title'],
                description=serializer.validated_data['description'],
                shorts=serializer.validated_data['shorts'],
                width=serializer.validated_data.get('width'),
                depth=serializer.validated_data.get('depth'),
                height=serializer.validated_data.get('height'),
                thumbnail_image=serializer.validated_data['thumbnail_image'],
                images=serializer.validated_data.get('images', []),
                categories=serializer.validated_data.get('categories', []),
                colors=serializer.validated_data.get('colors', []),
            )
            return Response({'message': 'success'})

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            seller_service = SellerService()
            seller_service.modify_item(
                seller_id=request.user.seller.seller_id,
                item_id=kwargs['item_id'],
                price=serializer.validated_data['price'],
                max_amount=serializer.validated_data['max_amount'],
                title=serializer.validated_data['title'],
                description=serializer.validated_data['description'],
                shorts=serializer.validated_data['shorts'],
                width=serializer.validated_data['width'],
                depth=serializer.validated_data['depth'],
                height=serializer.validated_data['height'],
                thumbnail_image=serializer.validated_data['thumbnail_image'],
                images=serializer.validated_data.get('images', []),
                tags=serializer.validated_data.get('tags', []),
            )
            return Response({'message': 'success'})


class SellerMyInfoView(APIView):
    permission_classes = [IsSeller]
    serializer_class = SellerMyInfoSerializer

    def get(self, request):
        seller = SellerRepository().get_seller_info(request.user.user_id)
        data = self.serializer_class(seller).data
        return Response(data, status=200)


class SellerInfoView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SellerInfoSerializer

    def get(self, request, *args, **kwargs):
        nickname = kwargs['nickname']
        seller = SellerRepository().get_seller_info_by_nickname(nickname)
        data = self.serializer_class(seller).data
        return Response(data, status=200)


class SellerDescriptionView(APIView):
    permission_classes = [IsSeller]
    serializer_class = DescriptionSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            seller_service = SellerService()
            seller_service.change_description(
                seller_id=request.user.seller.seller_id,
                description=serializer.validated_data['description'],
            )
            return Response({'message': 'success'})


class SellerMyOrderView(GenericAPIView):
    permission_classes = [IsSeller]
    serializer_class = SellerMyOrderSerializer
    filterset_class = SellerMyOrderFilterBackend

    def get(self, request):
        orders = self.filter_queryset(self.get_queryset())
        orders_data = self.serializer_class(orders, many=True).data
        return Response(orders_data, status=200)

    def get_queryset(self):
        order_repository = OrderRepository()
        return order_repository.get_order_list_by_seller(self.request.user.seller.seller_id)
