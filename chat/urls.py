from django.urls import path

from . import views

urlpatterns = [
    path("<str:room_name>/", views.room, name="room"),
    path("api/create_room/", views.create_room_id, name="create_room_id")
]