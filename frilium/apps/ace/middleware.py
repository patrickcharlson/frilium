from . import controller


def permission_middleware(get_response):
    def middleware(request):
        request.ace = controller.get_user_permissions(request.user, request.versions)
        return get_response(request)

    return middleware
