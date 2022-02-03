from django.core.cache import cache

from . import ACE_CACHE


def get_ace_cache(user, versions):
    key = get_cache_key(user, versions)
    return cache.get(key)


def get_cache_key(user, versions):
    return f'ace_{user.ace.key}_{versions[ACE_CACHE]}'
