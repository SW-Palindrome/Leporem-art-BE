from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .open_api_params import get_params
from .serializers import ConsentSerializer


# Create your views here.
class ConsentPrivacyView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(manual_parameters=get_params)
    def get(self):
        return Response('Description Test')

    @swagger_auto_schema(request_body=ConsentSerializer, responses={201: 'Success'})
    def post(self, request):
        consents = ConsentSerializer(data=request.data)
        if consents.is_valid():
            consents.save()
            return Response(consents.data)
        return Response(consents.errors, status=400)
