import re
from django.http import HttpResponseForbidden

class LinkBlockerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and 'content' in request.POST:
            message = request.POST['content']
            if re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message):
                    return HttpResponseForbidden('Ссылки не разрешены в сообщениях')
            else:
                return self.get_response(request)
        return self.get_response(request)
class WordsBlockerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and 'content' in request.POST:
            message = request.POST['content']
            # Регулярное выражение для блокировки матерных слов на русском и английском языках
            prohibited_words = [
                r'\bхуй\b', r'\bхуи\b', r'\bхуя\b', r'\bхуе\b', r'\bхуё\b', r'\bпизд\b',
                r'\bебан\b', r'\bбляд\b', r'\bебат\b', r'\bебу\b', r'\bfuck\b', r'\bshit\b', r'\bass\b',
                r'\bbitch\b', r'\bcunt\b', r'\bdick\b', r'\bpiss\b'
            ]
            pattern = re.compile('|'.join(prohibited_words), re.IGNORECASE)
            if pattern.search(message):
                return HttpResponseForbidden('Сообщение содержит запрещенные слова')
            else:
                return self.get_response(request)
        return self.get_response(request)