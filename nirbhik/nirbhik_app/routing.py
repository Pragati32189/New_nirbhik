from django.urls import path
from .consumers import UserLocationConsumer

websocket_urlpatterns = [
    path("ws/locations/", UserLocationConsumer.as_asgi()),
]
