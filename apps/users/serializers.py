from rest_framework import serializers


class ChangeNicknameSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=10)


class ChangeProfileImageSerializer(serializers.Serializer):
    profile_image = serializers.ImageField()


class UserInfoSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=20)
    profile_image = serializers.ImageField()
    is_seller = serializers.BooleanField()
