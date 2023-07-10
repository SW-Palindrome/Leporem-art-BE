from rest_framework import serializers


class SellerRegisterSerializer(serializers.Serializer):
    email = serializers.RegexField('^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9-]+\.)+ac\.kr$')


class SellerVerifySerializer(serializers.Serializer):
    verify_code = serializers.CharField(max_length=4)
