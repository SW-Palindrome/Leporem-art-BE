from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.deliveries.serializers import RegisterDeliveryInfoSerializer
from apps.deliveries.services import DeliveryService
from apps.users.permissions import IsSeller


class RegisterDeliveryInfoView(APIView):
    permission_classes = [IsSeller]
    serializer_class = RegisterDeliveryInfoSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        delivery_info = DeliveryService().register(
            user_id=request.user.user_id,
            order_id=serializer.validated_data['order_id'],
            delivery_company_name=serializer.validated_data['delivery_company'],
            invoice_number=serializer.validated_data['invoice_number'],
        )
        return Response({'delivery_info_id': delivery_info.delivery_info_id}, status=status.HTTP_201_CREATED)


class DeliveryInfoView(APIView):
    permission_classes = [IsSeller]

    def get(self, request, order_id):
        delivery_info = DeliveryService().get_delivery_info(user_id=request.user.user_id, order_id=order_id)
        if delivery_info is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(
            {
                'delivery_company': delivery_info.delivery_company.name,
                'invoice_number': delivery_info.invoice_number,
            }
        )


class DeliveryInfoTrackingUrlView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        tracking_url = DeliveryService().get_tracking_url(user_id=request.user.user_id, order_id=order_id)
        if tracking_url is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response({'delivery_tracking_url': tracking_url})
