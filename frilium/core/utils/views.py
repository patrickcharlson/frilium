def is_post(request):
    return request.method == 'POST'


def post_data(request):
    if is_post(request):
        return request.POST

    return None
