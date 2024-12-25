from django.http import HttpResponseForbidden

ALLOWED_IPS = ['127.0.0.1', '79.126.25.39']  # замените на ваши IP-адреса

class RestrictAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            ip = request.META.get('REMOTE_ADDR')
            if ip not in ALLOWED_IPS:
                return HttpResponseForbidden("Доступ запрещен.")
        response = self.get_response(request)
        return response