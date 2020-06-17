"""
Settings overrides for development.

"""
from .common import *  # noqa: F401,F403

INSTALLED_APPS += [
    "django_extensions",
]

ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http"
ACCOUNT_ADAPTER = "allauth.account.adapter.DefaultAccountAdapter"

try:
    from config.settings.local import *  # noqa: F401
except ImportError:
    pass
