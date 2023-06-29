from .base import *

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


# Sentry 설정
sentry_sdk.init(
    dsn="https://0f4e241425e74741a4f8340ab95c4ba9@app.glitchtip.com/3492",
    integrations=[DjangoIntegration()],
    auto_session_tracking=False,
    traces_sample_rate=0
)
