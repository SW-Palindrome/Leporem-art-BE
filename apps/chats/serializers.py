from rest_framework import serializers


class MessageListSerializer(serializers.Serializer):
    message_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    write_datetime = serializers.DateTimeField()
    text = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)


class BuyerChatRoomListSerializer(serializers.Serializer):
    chat_room_id = serializers.IntegerField()
    opponent_nickname = serializers.CharField()
    opponent_user_id = serializers.IntegerField()
    opponent_profile_image = serializers.ImageField(source='seller.user.profile_image')
    message_list = MessageListSerializer(many=True, source='messages')


class MessageCreateSerializer(serializers.Serializer):
    chat_room_id = serializers.IntegerField()
    text = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)

    def validate(self, attrs):
        if bool(attrs.get('text')) == bool(attrs.get('image')):
            raise serializers.ValidationError('text와 image 중 하나만 입력해주세요.')
        return attrs
