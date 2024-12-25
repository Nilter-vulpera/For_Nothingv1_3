"""
ASGI config for main project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path


from main.messages_main import routing  # замените "your_app" на имя вашего приложения

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
from main.messages_main.consumers import DialogConsumer
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws',DialogConsumer.as_asgi() )
            ]
        )
    ),
})
