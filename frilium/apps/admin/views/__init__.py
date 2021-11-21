from django.urls import reverse, NoReverseMatch

from frilium.apps.core.conf import settings


def get_protected_namespace(request):
    for namespace in settings.FRILIUM_ADMIN_NAMESPACES:
        try:
            admin_path = reverse(f'{namespace}:dashboard')
            if request.path.startswith(admin_path):
                return namespace
        except NoReverseMatch:
            pass
