from rest_framework import serializers


class BuyerChatRoomListSerializer(serializers.Serializer):
    chat_room_id = serializers.IntegerField()
    opponent_nickname = serializers.CharField()
    opponent_profile_image = serializers.ImageField(source='seller.user.profile_image')
    last_message = serializers.CharField()
    last_message_datetime = serializers.DateTimeField()
