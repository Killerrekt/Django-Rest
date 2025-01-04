from rest_framework.response import Response
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password,check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from .models import User,Article
from .serializer import UserSerializer

#Feature list:-
gen_feature = False
tag_feature = False

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
    msg = {"message":"Secret Message","data":UserSerializer(request.info).data}
    return Response(data=msg)

@api_view(['POST'])
def CreateUser(request):
    data = request.data
    username = data.get('name')
    email = data.get('email')
    password = make_password(data.get('password'))
    role = data.get('role')
    if role not in ['admin','member']:
        return Response(data={"message":"the role can only be either admin or member"},status=400)
    try:
        User.objects.create(name = username, password = password,email = email,role = role)
    except IntegrityError as e:
        return Response(data={"message":"missing some data or email is in use", "error":str(e)},status=400)
    except Exception as e:
        return Response(data = {"message":"something went wrong will inserting into the database","error":e},status=500)
    return Response({"message" : "User created successfully"})

@api_view(['GET'])
def ServerFeatureStatus(request):
    return Response(data={"message" : "Successfully got the feature details","data":{
        "article_generation" : gen_feature,
        "tag_generation" : tag_feature
    }})
    
@api_view(['POST'])
def SetFeatureFlag(request):
    global gen_feature, tag_feature
    
    data = request.data
    gen = data.get('gen_feature')
    if gen in [True,False]:
        gen_feature = gen
    tag = data.get('tag_feature')
    if tag in [True,False]:
        tag_feature = tag
    return Response({"message":"Updated the flag"})

@api_view(['POST'])
def CreateArticle(request):
    data = request.data
    title = data.get("title")
    content = data.get("content")
    tags = data.get("tags")
    author = data.get("author")
    try:
        Article.objects.create(title=title,content=content,tags=tags,author=User.objects.filter(id=author).first())
    except Exception as e:
        return Response({"message":"Failed to create the article","error":str(e)},status=500)
    return Response({"message":"Article created successfully"})

@api_view(['PUT'])
def UpdateArticle(request):
    data = request.data
    title = data.get("title")
    content = data.get("content")
    tags = data.get("tags")
    author = data.get("author")
    id = data.get("id")
    try:
        article = Article.objects.filter(id=id).first()
        article.title = title
        article.content = content
        article.tags = tags
        article.author = User.objects.filter(id=author).first()
        article.save()
    except Exception as e:
        return Response({"message":"Failed to  the article","error":str(e)},status=500)
    return Response({"message":"Article Updated successfully"})

@api_view(['DELETE'])
def DeleteArticle(request):
    data = request.data
    id = data.get("id")
    try:
        Article.objects.filter(id = id).delete()
    except Exception as e:
        return Response({"message":"Failed to delete the article", "error":str(e)},status=500)
    return Response({"message":"Article deleted successfully"})