import json
import logging

import boto3

from apps.notifications.repositories import DeviceRepository
from apps.users.models import User

logger = logging.Logger(__name__)


class NotificationService:
    def register_device(self, user, fcm_token):
        device_repository = DeviceRepository()
        if device_repository.get_devices(user, fcm_token):
            return True
        if device_repository.get_devices_by_token(fcm_token):
            device_repository.delete_device(fcm_token)
        device_repository.register(user, fcm_token)

    def send_to_specific_device(self, token, title, body, deep_link):
        lambda_client = boto3.client('lambda', region_name='ap-northeast-2')
        lambda_client.invoke(
            FunctionName='fcmPushAlarm',
            InvocationType='Event',
            Payload=json.dumps(
                {
                    'token': token,
                    'title': title,
                    'body': body,
                    'deep_link': deep_link,
                }
            ),
        )

    def send(self, user: User, title: str, body: str, deep_link: str):
        devices = DeviceRepository().get_devices_by_user(user)
        for device in devices:
            self.send_to_specific_device(device.fcm_token, title, body, deep_link)
