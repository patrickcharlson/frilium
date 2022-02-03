from importlib import import_module

from frilium.apps.core.conf import settings

_NOT_INITIALIZED_ERROR = (
    "PermissionApplicators instance has to load applicators with load() "
    "before get_obj_type_annotators(), get_user_acl_serializers(), "
    "list() or dict() methods will be available."
)


class PermissionApplicators:
    def __init__(self):
        self._initialized = False
        self._applicators = []
        self._applicators_dict = {}

        self._annotators = {}
        self._user_ace_serializers = []

    def load(self):
        if self._initialized:
            raise RuntimeError('Applicators are already provided')

        self._register_applicators()

    def _register_applicators(self):
        for applicator in settings.FRILIUM_APPLICATORS:
            self._applicators.append((applicator, import_module(applicator)))

    def list(self):
        assert self._initialized, _NOT_INITIALIZED_ERROR
        return self._applicators


applicators = PermissionApplicators()
