"""
ASGI config for jatte project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from chat.routing import websockert_urlpattern

from channels.routing import ProtocolTypeRouter , URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jatte.settings')

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket" : AuthMiddlewareStack(
            URLRouter(
                websockert_urlpattern
            )
        )
        # Just HTTP for now. (We can add other protocols later.)
    }
)