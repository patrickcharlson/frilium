from django.core.cache import cache

from . import ACE_CACHE


def get_ace_cache(user, versions):
    key = get_cache_key(user, versions)
    return cache.get(key)


def set_ace_cache(user, versions, user_access):
    key = get_cache_key(user, versions)
    cache.set(key, user_access)


def get_cache_key(user, versions):
    return f'ace_{user.ace.key}_{versions[ACE_CACHE]}'
