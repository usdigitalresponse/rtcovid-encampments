"""
Settings overrides for development.

"""
from .common import *  # noqa: F401,F403

INSTALLED_APPS += [
    "django_extensions",
]


try:
    from config.settings.local import *  # noqa: F401
except ImportError:
    pass
