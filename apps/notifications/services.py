from firebase_admin import messaging

from apps.notifications.repositories import DeviceRepository


class NotificationService:
    def register_device(self, user, fcm_token):
        device_repository = DeviceRepository()
        device_repository.register(user, fcm_token)

    def send_to_specific_device(self, token, title, body, deep_link):
        registration_token = token
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=registration_token,
            data={
                "url": deep_link,
            },
        )
        return message

    def send_to_multiple_devices(self, tokens, title, body, deep_link):
        registration_tokens = list(tokens)
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            tokens=registration_tokens,
            data={
                "url": deep_link,
            },
        )
        return message
