def permission_middleware(get_response):
    def middleware(request):
        request.ace = ''
