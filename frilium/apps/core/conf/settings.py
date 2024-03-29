from django.conf import settings as frilium_settings

from . import defaults


class Settings:

    def __getattr__(self, item):
        try:
            return getattr(frilium_settings, item)
        except AttributeError:
            return getattr(defaults, item)
