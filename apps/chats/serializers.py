import pytz
from rest_framework import serializers

from apps.chats.models import Message


class MessageSerializer(serializers.Serializer):
    message_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    write_datetime = serializers.DateTimeField(default_timezone=pytz.timezone('Asia/Seoul'))
    is_read = serializers.BooleanField()
    message = serializers.CharField()
    uuid = serializers.UUIDField()
    type = serializers.CharField()


class BuyerChatRoomListAllMessagesSerializer(serializers.Serializer):
    chat_room_id = serializers.IntegerField()
    opponent_nickname = serializers.CharField()
    opponent_user_id = serializers.IntegerField()
    opponent_profile_image = serializers.ImageField(source='seller.user.profile_image')
    message_list = MessageSerializer(many=True, source='messages')
    uuid = serializers.UUIDField()


class BuyerChatRoomListSerializer(serializers.Serializer):
    chat_room_id = serializers.IntegerField()
    opponent_nickname = serializers.CharField()
    opponent_user_id = serializers.IntegerField()
    opponent_profile_image = serializers.ImageField(source='seller.user.profile_image')
    last_message = MessageSerializer()
    unread_count = serializers.IntegerField()
    uuid = serializers.UUIDField()


class SellerChatRoomListAllMessagesSerializer(serializers.Serializer):
    chat_room_id = serializers.IntegerField()
    opponent_nickname = serializers.CharField()
    opponent_user_id = serializers.IntegerField()
    opponent_profile_image = serializers.ImageField(source='buyer.user.profile_image')
    message_list = MessageSerializer(many=True, source='messages')
    uuid = serializers.UUIDField()


class SellerChatRoomListSerializer(serializers.Serializer):
    chat_room_id = serializers.IntegerField()
    opponent_nickname = serializers.CharField()
    opponent_user_id = serializers.IntegerField()
    opponent_profile_image = serializers.ImageField(source='buyer.user.profile_image')
    last_message = MessageSerializer()
    unread_count = serializers.IntegerField()
    uuid = serializers.UUIDField()


class BuyerChatRoomCreateSerializer(serializers.Serializer):
    seller_id = serializers.IntegerField()
    text = serializers.CharField(required=False)
    image = serializers.CharField(required=False)
    chat_room_uuid = serializers.UUIDField(required=False)
    message_uuid = serializers.UUIDField(required=False)
    message_type = serializers.ChoiceField(choices=Message.Type, default=Message.Type.TEXT)

    def validate(self, attrs):
        if bool(attrs.get('text')) == bool(attrs.get('image')):
            raise serializers.ValidationError('text와 image 중 하나만 입력해주세요.')
        return attrs


class MessageCreateSerializer(serializers.Serializer):
    chat_room_uuid = serializers.UUIDField()
    text = serializers.CharField(required=False)
    image = serializers.CharField(required=False)
    message_uuid = serializers.UUIDField(required=False)
    type = serializers.ChoiceField(choices=Message.Type, default=Message.Type.TEXT)

    def validate(self, attrs):
        if bool(attrs.get('text')) == bool(attrs.get('image')):
            raise serializers.ValidationError('text와 image 중 하나만 입력해주세요.')
        return attrs


class MessageReadSerializer(serializers.Serializer):
    chat_room_uuid = serializers.UUIDField()
    message_uuid = serializers.UUIDField()
