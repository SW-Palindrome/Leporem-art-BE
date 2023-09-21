from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.notifications.serializers import DeviceSerializer
from apps.notifications.services import NotificationService


class DeviceRegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = DeviceSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            notification_service = NotificationService()
            notification_service.register_device(user=request.user.user_id, fcm_token=request.data.get('fcm_token'))
            return Response({'message': 'success'}, status=201)
        return Response({'message': 'failed'}, status=400)


class SpecificNotificationView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        notification_service = NotificationService()
        notification_service.send_to_specific_device(
            token=request.GET.get('token'),
            title=request.GET.get('title'),
            body=request.GET.get('body'),
            deep_link=request.GET.get('deep_link'),
        )
        return Response({'message': 'success'}, status=200)
