from rest_framework import serializers
from .models import *

class UserRegistrationSerializer(serializers.ModelSerializer):
       
    def create(self, validated_data):
        user=User.objects.create_user(**validated_data)
        return user
    
    class Meta:
        model = User
        fields = ["email", "username" , "password"]


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField()
    
    class Meta:
        model = User
        fields = ["email", "password"]

class RecordSerializer(serializers.ModelSerializer):

    class Meta:
        model=Records
        field=['right_count',"wrong_count"]

class QuestionSerializer(serializers.ModelSerializer):
    ques=serializers.StringRelatedField()
    class Meta:
        model=Answers
        fields=['ques', 'answer','label']