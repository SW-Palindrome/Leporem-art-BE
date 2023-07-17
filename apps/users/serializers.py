from rest_framework import serializers

from .models import User


class ChangeNicknameSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=10)
