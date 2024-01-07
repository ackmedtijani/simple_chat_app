from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from account.models import Token

from .models import Room

import json

# Create your views here.

@csrf_exempt
def room(request , room_name):
    return render(request , "room.html" , context={"room_name" : room_name})

@csrf_exempt
@require_POST
def create_room_id(request):
    headers = request.META.get('HTTP_AUTHORIZATION')
    print("token" , headers , request.META)
    username = json.loads(request.body).get("room_name" , "Default Room name")
    
    if headers:
        headers = headers.split(" ")[1]
        print("headers" , headers)
        try:
            token = Token.objects.get(token = headers)
        except Token.DoesNotExist:
            return JsonResponse({"error" : "No user found for this token"})
        

        room = Room.objects.create(name = username)
        room.participitants.add(token.user)

        room.save()

        return JsonResponse({"room_id" : room.id})
    
        
            

    return JsonResponse({"error" : "No token in header"})