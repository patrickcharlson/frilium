import typing as t

from django.utils.decorators import classonlymethod
from django.views import View


def is_post(request):
    return request.method == 'POST'


def post_data(request):
    if is_post(request):
        return request.POST

    return None
