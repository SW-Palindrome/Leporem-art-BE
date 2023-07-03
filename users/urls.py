from django.urls import path
from src.users.views import ConsentPrivacyView

urlpatterns = [
    path('v1/consent-privacy/', ConsentPrivacyView.as_view(), name='consent-privacy')
]
