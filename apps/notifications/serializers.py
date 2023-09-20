from rest_framework import serializers


class DeviceSerializer(serializers.Serializer):
    fcm_token = serializers.CharField(max_length=255)
