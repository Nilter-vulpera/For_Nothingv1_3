from django.urls import path, re_path

from . import consumers

websocket_urlpatterns = [
    path(r'^dialogs/(?P<chat_id>\d+)/$', consumers.DialogConsumer.as_asgi()),
]
