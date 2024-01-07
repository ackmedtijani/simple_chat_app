from django.urls import path

from . import consumer

websockert_urlpattern = [
    path("ws/chat/<str:room_name>/<str:api_key>/", consumer.ChatConsumer.as_asgi()),
    path("ws/read_receipt/<str:room_name>/<str:api_key>/", consumer.ReadReceiptConsumer.as_asgi())
]