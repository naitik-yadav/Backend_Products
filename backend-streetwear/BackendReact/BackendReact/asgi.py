"""
ASGI config for BackendReact project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from Demoapp import consumers  

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BackendReact.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Regular HTTP routing
    "websocket": URLRouter([
        path("ws/nike_updates/", consumers.NikeConsumer.as_asgi()),
    ]),
})