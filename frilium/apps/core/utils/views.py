import typing as t

from django.utils.decorators import classonlymethod
from django.views import View


def is_post(request):
    return request.method == 'POST'


def post_data(request):
    if is_post(request):
        return request.POST

    return None


class MethodView(View):
    decorators: t.List[t.Callable] = []

    @classonlymethod
    def as_view(cls, **initkwargs):
        super().as_view(**initkwargs)
        if cls.decorators:
            cls.view.__module__ = cls.__module__
            for decorator in cls.decorators:
                view = decorator(cls.view)

