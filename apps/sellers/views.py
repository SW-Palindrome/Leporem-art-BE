from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.sellers.serializers import SellerRegisterSerializer, SellerVerifySerializer
from apps.sellers.services import SellerRegisterService


class SellerRegisterView(APIView):
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
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
