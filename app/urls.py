from django.urls import path,include
from .views import *
urlpatterns = [
    path("register/",register),
    path("login/",login),
    path("get_question/",get_question),
]