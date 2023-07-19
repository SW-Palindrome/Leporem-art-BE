from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.sellers.repositories import SellerRepository
from apps.sellers.serializers import (
    SellerInfoSerializer,
    SellerItemSerializer,
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
                width=serializer.validated_data['width'],
                depth=serializer.validated_data['depth'],
                height=serializer.validated_data['height'],
                thumbnail_image=serializer.validated_data['thumbnail_image'],
                images=serializer.validated_data.get('images', []),
                tags=serializer.validated_data.get('tags', []),
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
    serializer_class = SellerInfoSerializer

    def get(self, request):
        user = SellerRepository().get_seller_info(request.user.user_id)
        data = self.serializer_class(user).data
        return Response(data, status=200)
