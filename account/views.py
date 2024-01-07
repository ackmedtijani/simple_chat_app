from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import json

from .models import Token, User

# Create your views here.

@csrf_exempt
@require_POST
def create_token(request):
    data = json.loads(request.body)
    try:
        email = data["email"]
        password = data.get("password")

        if not password:
            password = "1234567"
            
    except Exception as e:
        return JsonResponse({"detail" : f"Missing values{str(e)}" } , status = 400)
    
    
    user = User.objects.create(email = email , password = password )
    token = Token.objects.create(user = user)

    return JsonResponse({"detail" : "success. User created" , "token" : token.token })