from django.urls import path,include
from .views import *
urlpatterns = [
    path("register/",register),
    path("login/",login),
    path("get_question/",get_question),
    path("update_record/",update_records),
    # path('api-token-auth/', CustomAuthToken.as_view())
]