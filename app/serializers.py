from rest_framework import serializers
from .models import *

class UserRegistrationSerializer(serializers.ModelSerializer):
    
    confirm_password= serializers.CharField(style={"input_type": "password"}, write_only=True)   
        
    def validate(self, data):
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        if password != confirm_password:
            raise serializers.ValidationError("Password must match")
        return data
    
    
    def create(self, validated_data):
        user=User.objects.create_user(**validated_data)
        return user
    
    class Meta:
        model = User
        fields = ["email", "username" , "password","confirm_password"]


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
    class Meta:
        model=Answers
        fields=['question', 'answer','label' ]