from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('ping/',views.Ping),
    path('signup/',views.SignUp),
    path('login/',views.Login),
    path('protected/',views.Protected),
    path('refresh/',TokenRefreshView.as_view())
]
