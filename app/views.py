from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .serializers import *

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
            return Response({'msg':'user login sucessful'}, status=status.HTTP_200_OK)
        return Response({'msg':'authentication error'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_question(request):
    serializer=QuestionSerializer(data=request.data)
    # if serializer.is_valid():
           




