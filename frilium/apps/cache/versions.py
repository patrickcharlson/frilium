from frilium.apps.cache.models import CacheVersion


def get_cache_versions():
    qs = CacheVersion.objects.all()
    return {i.name: i.version for i in qs}
