from hashlib import md5
from time import time

from django.contrib import auth as dj_auth, messages

from frilium.apps.core.conf import settings

TOKEN_KEY = 'frilium_admin_session_token'
UPDATED_KEY = 'frilium_admin_session_updated'


def is_admin_authorized(request):
    if request.user.is_anonymous:
        return False

    if not request.user.is_staff:
        return False

    admin_token = request.session.get(TOKEN_KEY)
    if not admin_token == make_user_admin_token(request.user):
        return False

    updated = request.session.get(UPDATED_KEY, 0)
    if updated < time() - (settings.FRILIUM_ADMIN_SESSION_EXPIRATION * 60):
        if updated:
            request.session.pop(UPDATED_KEY, None)
            messages.info(request, 'Your Admin session has expired.')
        return False

    return True


def update_admin_authorization(request):
    request.session[UPDATED_KEY] = int(time())


def remove_admin_authorization(request):
    request.session.pop(TOKEN_KEY, None)
    request.session.pop(UPDATED_KEY, None)


def make_user_admin_token(user):
    formula = (str(user.pk), user.email, user.password, settings.SECRET_KEY)
    return md5(":".join(formula).encode()).hexdigest()


login = dj_auth.login
