from rest_framework import serializers

from .models import User


# ConsentPrivacy
class ConsentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_agree_privacy', 'is_agree_ads']
