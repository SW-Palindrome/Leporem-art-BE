import logging

import requests
from django.conf import settings
from google.auth.transport import requests as auth_requests
from google.oauth2 import service_account

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
        credentials = service_account.Credentials.from_service_account_info(
            settings.FIREBASE_CONFIG, scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
        credentials.refresh(auth_requests.Request())
        response = requests.post(
            settings.FIREBASE_MESSAGE_SEND_URL,
            json={
                'validate_only': False,
                'message': {
                    'data': {
                        "url": deep_link,
                    },
                    'notification': {
                        'title': title,
                        'body': body,
                    },
                    'token': token,
                    'webpush': {},
                    'fcm_options': {},
                },
            },
            headers={
                'Authorization': f'Bearer {credentials.token}',
            },
        )
        # FCM Token 중복 시 404 응답
        if not response.status_code not in {200, 404}:
            logger.error(f'Failed to send notification to {token} with status code {response.status_code}')

    def send(self, user: User, title: str, body: str, deep_link: str):
        devices = DeviceRepository().get_devices_by_user(user)
        for device in devices:
            self.send_to_specific_device(device.fcm_token, title, body, deep_link)
