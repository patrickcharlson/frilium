from . import generator
from .cache import get_ace_cache, set_ace_cache


def get_user_permissions(user, versions):
    user_access = get_ace_cache(user, versions)
    if user_access is None:
        user_access = generator.generate_ace(user.get_roles())
        set_ace_cache(user, versions, user_access)
    user_access['user_id'] = user.id
    user_access['is_authenticated'] = bool(user.is_authenticated)
    user_access['is_anonymous'] = bool(user.is_anonymous)
    user_access['is_staff'] = user.is_staff
    user_access['is_superuser'] = user.is_superuser
    user_access['versions'] = versions.copy()
    return user_access

