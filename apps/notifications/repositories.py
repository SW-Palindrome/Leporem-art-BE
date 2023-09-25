from apps.notifications.models import Device
from apps.users.models import User


class DeviceRepository:
    def register(self, user_id, fcm_token):
        user = User.objects.get(user_id=user_id)
        return Device.objects.create(user=user, fcm_token=fcm_token)

    def get_devices_by_user(self, user):
        return Device.objects.filter(user=user)

    def get_devices_by_token(self, fcm_token):
        return Device.objects.filter(fcm_token=fcm_token)

    def get_devices(self, user, fcm_token):
        return Device.objects.filter(user=user, fcm_token=fcm_token)

    def delete_device(self, fcm_token):
        return Device.objects.filter(fcm_token=fcm_token).delete()
