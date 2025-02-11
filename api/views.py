from rest_framework.response import Response
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password,check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from .models import User,Article,Comment
from .serializer import UserSerializer,ArticleSerializer,CommentPopulatedArticleSerializer
from .gen_api import GenApi

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
    generate_content = data.get("generate_article")
    generate_tags = data.get("generate_tag")
    tags = data.get("tags")
    author = request.info.id
    text_content = "Can u generate a article on {title} and in plain text no need for markdown".format(title = title)
    if generate_content == True:
        if gen_feature:
            content = GenApi(text_content)
        else:
            return Response({"message" : "Gen article feature is disabled"})
    if generate_tags == True:
        if tag_feature:
            text_tag = "Can u generate appropriate tags for the following article. It shld be , separated.{content}".format(content = content)
            tags = GenApi(text_tag)
        else:
            return Response({"message":"Tag feature is disabled"})
    try:
        article = Article.objects.create(title=title,content=content,tags=tags,author=User.objects.filter(id=author).first())
    except Exception as e:
        return Response({"message":"Failed to create the article","error":str(e)},status=500)
    return Response({"message":"Article created successfully","data" :ArticleSerializer(article).data})

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

@api_view(['GET'])
def GetAllArticle(request):
    try:
        articles = Article.objects.all()
        data = ArticleSerializer(articles,many=True)
    except Exception as e:
        return Response({"message":"Failed to get the articles","error":str(e)},status=500)
    return Response({"message":"Successfully got the articles","data":data.data})

@api_view(['GET'])
def GetArticle(request):
    id = request.query_params.get("id")
    try:
        articles = Article.objects.filter(id = id).first()
        data = CommentPopulatedArticleSerializer(articles)
    except Exception as e:
        return Response({"message":"Failed to get the article","error":str(e)},status=500)
    return Response({"message":"Successfully got the article","data":data.data})

@api_view(['POST'])
def WriteComment(request):
    data = request.data
    content = data.get('content')
    article = Article.objects.filter(id = data.get('article')).first()
    user = User.objects.filter(id = request.info.id).first()
    try:
        Comment.objects.create(content = content,article = article,user = user)
    except Exception as e:
        return Response({"message":"Failed to save the comment","error":str(e)},status=500)
    return Response({"message":"comment saved successfully"})
    
@api_view(['POST'])
def GenArticle(request):
    prompt = request.data.get('prompt')
    return Response({"message":"Success","data":GenApi(prompt)})