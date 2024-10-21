from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .serializers import *
from .models import Questions, Answers
import random


# class CustomAuthToken(ObtainAuthToken):

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key,
#             'user_id': user.pk,
#             'email': user.email
#         })

@api_view(['POST'])
def register(request):
    serializer=UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response ({"msg":"user registered sucessfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    serializer=UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        email=serializer.data.get('email')
        print(email)
        password=serializer.validated_data.get('password')
        print(password)
        user=authenticate(email=email, password=password)
        if user :
            print(user)
            token, _created=Token.objects.get_or_create(user=user)
            print(token)
            print(user.auth_token.key)  
            return Response({'msg':'user login sucessful', 'token':token.key}, status=status.HTTP_200_OK)
        return Response({'msg':'authentication error'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes(IsAuthenticated)
@api_view(['GET'])
def get_question(request):
    question=random.choice(Questions.objects.all())
    try:
        answer=Answers.objects.filter(question=question)
        if not answer.exists(): 
            return Response({"error": "No answers found for the selected question"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = QuestionSerializer(answer, many=True) 
        
        return Response({'question':question.question,'answers':serializer.data}, status=status.HTTP_200_OK)
    except Answers.DoesNotExist:
        return Response({"error": "No answer found for the selected question"}, status=status.HTTP_404_NOT_FOUND)


# @permission_classes(IsAuthenticated)
# @api_view(['POST'])
# def check_answer


@permission_classes(IsAuthenticated)   
@api_view(['POST'])
def update_records(request):
    # import ipdb
    # ipdb.set_trace()
    user=request.user
    if not user:
        return Response({"msg":"User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    record,created=Records.objects.get_or_create(related_user=user,defaults={'right_count':request.data.get('right_count'), 'wrong_count':request.data.get('wrong_count')})
    if not created:
        record.right_count=request.data.get('right_count')
        record.wrong_count=request.data.get('wrong_count')
    record.save()
    return Response({'msg':'record updated sucessfully'},status=status.HTTP_200_OK)
    



