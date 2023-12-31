from django.urls import path

from apps.notifications.views import DeviceRegisterView, SpecificNotificationView

urlpatterns = [
    path('register', DeviceRegisterView.as_view()),
    path('specific', SpecificNotificationView.as_view()),
]
