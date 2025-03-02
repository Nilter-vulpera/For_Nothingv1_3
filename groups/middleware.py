import re
from django.http import HttpResponseForbidden

class LinkBlockerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and 'contentForPosts' in request.POST:
            message = request.POST['contentForPosts']
            if re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message):
                    return HttpResponseForbidden('Ссылки не разрешены в сообщениях')
            else:
                return self.get_response(request)
        return self.get_response(request)