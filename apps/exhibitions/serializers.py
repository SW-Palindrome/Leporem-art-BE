from rest_framework import serializers


class ExhibitionSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=20)
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
