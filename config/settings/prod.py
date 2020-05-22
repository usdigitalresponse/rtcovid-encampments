"""
Settings overrides for production.

"""
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .common import *  # noqa: F401,F403

DEBUG = False

ALLOWED_HOSTS = ["coo-encampments.rtcovid.com"]

sentry_sdk.init(
    dsn="https://69c5541e25bf43a6a52f31d9c2a887eb@o379494.ingest.sentry.io/5236469",
    integrations=[DjangoIntegration()],
    send_default_pii=True,
)
