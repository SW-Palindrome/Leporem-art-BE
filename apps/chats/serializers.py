from rest_framework import serializers


class BuyerChatRoomListSerializer(serializers.Serializer):
    chat_room_id = serializers.IntegerField()
    opponent_nickname = serializers.CharField()
    opponent_profile_image = serializers.ImageField(source='seller.user.profile_image')
    last_message = serializers.CharField()
    last_message_datetime = serializers.DateTimeField()


class MessageCreateSerializer(serializers.Serializer):
    chat_room_id = serializers.IntegerField()
    text = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)

    def validate(self, attrs):
        if bool(attrs.get('text')) == bool(attrs.get('image')):
            raise serializers.ValidationError('text와 image 중 하나만 입력해주세요.')
        return attrs
