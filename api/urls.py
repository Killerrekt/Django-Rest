from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('ping/',views.Ping),
    path('signup/',views.SignUp),
    path('login/',views.Login),
    path('protected/',views.Protected),
    path('refresh/',TokenRefreshView.as_view()),
    path('feature/',views.ServerFeatureStatus),
    
    path('owner/create-user/',views.CreateUser),
    path('owner/set-flag/',views.SetFeatureFlag),
    
    path('admin/create-article/',views.CreateArticle),
    path('admin/update-article/',views.UpdateArticle),
    path('admin/delete-article/',views.DeleteArticle),
    
    path('article-all/',views.GetAllArticle),
    path('article/',views.GetArticle)
]
