from django.urls import path
from . import views

urlpatterns = [
    path('ping/',views.Ping),
    path('signup/',views.SignUp)
]
