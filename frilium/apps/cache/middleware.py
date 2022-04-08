from .versions import get_cache_versions


def cache_version_middleware(get_response):
    def middleware(request):
        request.versions = get_cache_versions()
        return get_response(request)

    return middleware
