import pytz
from rest_framework import serializers


class ExhibitionSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=20)
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()


class ExhibitionIntroductionSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=46)
    cover_image = serializers.ImageField()
    artist_name = serializers.CharField(max_length=100)


class ExhibitionArtistRegisterSerializer(serializers.Serializer):
    is_template = serializers.BooleanField()
    artist_image = serializers.ImageField()
    biography = serializers.CharField(max_length=255, allow_null=True, required=False)
    font_family = serializers.CharField(max_length=50, allow_null=True, required=False)
    background_color = serializers.CharField(max_length=10, allow_null=True, required=False)

    def validate(self, attrs):
        if attrs['is_template'] and not all(
            [attrs.get('biography'), attrs.get('font_family'), attrs.get('background_color')]
        ):
            raise serializers.ValidationError('템플릿을 사용할 경우, biography, font_family, background_color는 필수값입니다.')
        return attrs


class ExhibitionsSerializer(serializers.Serializer):
    exhibition_id = serializers.IntegerField()
    title = serializers.CharField()
    cover_image = serializers.ImageField()
    artist_name = serializers.CharField()
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()


class ExhibitionDetailInfoSerializer(serializers.Serializer):
    title = serializers.CharField()
    cover_image = serializers.ImageField()
    artist_name = serializers.CharField()
    biography = serializers.CharField()
    start_date = serializers.DateTimeField(default_timezone=pytz.timezone('Asia/Seoul'))
    end_date = serializers.DateTimeField(default_timezone=pytz.timezone('Asia/Seoul'))


class ExhibitionArtistInfoSerializer(serializers.Serializer):
    artist_image = serializers.ImageField()
    is_template = serializers.BooleanField()
    biography = serializers.CharField()
    font_family = serializers.CharField()
    background_color = serializers.CharField()


class ExhibitionItemInfoSerializer(serializers.Serializer):
    exhibition_item_id = serializers.IntegerField()
    item_id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()
    template = serializers.IntegerField()
    is_sale = serializers.BooleanField()
    background_color = serializers.CharField()
    font_family = serializers.CharField()
    is_custom = serializers.BooleanField()
    images = serializers.ListField(child=serializers.ImageField())
    sounds = serializers.ListField(child=serializers.FileField())
