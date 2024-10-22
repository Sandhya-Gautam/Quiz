from django.urls import path

from .views import check_answer, get_question, login, register

urlpatterns = [
    path("register/", register),
    path("login/", login),
    path("get_question/", get_question),
    path("check_answer/", check_answer),
]
