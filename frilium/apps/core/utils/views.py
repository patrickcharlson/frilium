from django.template.defaultfilters import slugify as frilium_slugify
from unidecode import unidecode


def is_post(request):
    return request.method == 'POST'


def post_data(request):
    if is_post(request):
        return request.POST

    return None


def slugify(string):
    string = str(string)
    string = unidecode(string)
    return frilium_slugify(string.replace("_", " ").strip())
