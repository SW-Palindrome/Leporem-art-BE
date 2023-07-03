from django.urls import path
from users.views import ConsentPrivacyView

urlpatterns = [
    path('v1/consent-privacy/', ConsentPrivacyView.as_view(), name='consent-privacy')
]
