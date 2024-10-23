from django.urls import path

from .views import CheckAnswer, GetQuestion, UserLogin, UserRegister

# from .views import check_answer, get_question, login, register

# urlpatterns = [
#     path("register/", register),
#     path("login/", login),
#     path("get_question/", get_question),
#     path("check_answer/", check_answer),
# ]

urlpatterns = [
    path("login/", UserLogin.as_view()),
    path("register/", UserRegister.as_view()),
    path("get_question/", GetQuestion.as_view()),
    path("check_answer/", CheckAnswer.as_view()),
]
