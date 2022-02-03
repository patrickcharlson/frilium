from . import generator
from .cache import get_ace_cache


def get_user_permissions(user, versions):
    user_access = get_ace_cache(user, versions)
    if user_access is None:
        user_access = generator.generate_ace(user.get_roles())
