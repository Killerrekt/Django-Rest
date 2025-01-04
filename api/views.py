from rest_framework.response import Response
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password,check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from .models import User
from .serializer import UserSerializer

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

@api_view(['POST'])
def Login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        user = User.objects.filter(email=email).first()
        check = check_password(password,user.password)
        print(check)
        if not user or not check:
            return Response(data = {"message":"invalid email or password"},status=400)
    except Exception as e:
        return Response(data = {"message":"something went wrong","error":str(e)},status=500)
    
    refresh = RefreshToken.for_user(user)
    return Response({
        "message" : "logged in successfully",
        "data":{
            'refresh': str(refresh),
            'access': str(refresh.access_token),
    }})
    
@api_view(['GET'])
def Protected(request):
    print(request.user)
    msg = {"message":"Secret Message","data":UserSerializer(request.info).data}
    return Response(msg)