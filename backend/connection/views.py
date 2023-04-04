from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def aPage(request):
    SingleUser:User = User.objects.get(pk=1)
    UserName =request.Post.get("UserName")
    Password =request.Post.get("Password")
    return JsonResponse({"UserName":"Aniraj",
                         "UName":UserName,
                         "Password": Password})
