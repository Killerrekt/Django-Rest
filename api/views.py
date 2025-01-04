from rest_framework.response import Response
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view
from .models import User

@api_view(['GET'])
def Ping(request):
    msg = {"message":"Pong"}
    return Response(msg)

@api_view(['POST'])
def SignUp(request):
    data = request.data
    username = data.get('name')
    email = data.get('email')
    password = make_password(data.get('password'))
    users = User.objects.all()
    if(len(users) == 0):
        role = "owner"
    else:
        role = "member"
    try:
        User.objects.create(name = username, password = password,email = email,role = role)
    except IntegrityError as e:
        return Response(data={"message":"missing some data or email is in use", "error":str(e)},status=400)
    except Exception as e:
        return Response(data = {"message":"something went wrong will inserting into the database","error":e},status=500)
    return Response({"message" : "User signup successfully"})