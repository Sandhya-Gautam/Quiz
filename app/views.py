import random

from django.contrib.auth import authenticate
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Answers, Questions, Records
from .serializers import (
    QuestionSerializer,
    UserLoginSerializer,
    UserRegistrationSerializer,
)


class UserLogin(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get("email")
            password = serializer.validated_data.get("password")
            user = authenticate(email=email, password=password)
            if user:
                token, _created = Token.objects.get_or_create(user=user)
                return Response(
                    {"msg": "user login sucessful", "token": token.key},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"msg": "authentication error"}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegister(APIView):
    def post(self, request):
        import ipdb

        ipdb.set_trace()
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "user registered sucessfully"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetQuestion(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        ids = Questions.objects.values("id")
        question_id = random.choice(ids)
        question = Questions.objects.get(id=question_id["id"])
        try:
            answer = Answers.objects.filter(question=question)
            if not answer.exists():
                return Response(
                    {"error": "No answers found for the selected question"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            serializer = QuestionSerializer(answer, many=True)

            return Response(
                {"question": question.question, "answers": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Answers.DoesNotExist:
            return Response(
                {"error": "No answer found for the selected question"},
                status=status.HTTP_404_NOT_FOUND,
            )


class CheckAnswer(APIView):
    permission_classes([permissions.IsAuthenticated])

    def post(self, request):
        answer = Answers.objects.get(id=request.data.get("id"))
        user = request.user
        if not user:
            return Response({"msg": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        if answer.label:
            record, created = Records.objects.get_or_create(
                related_user=user, defaults={"right_count": "1", "wrong_count": "0"}
            )
            if not created:
                record.right_count += 1
        else:
            record, created = Records.objects.get_or_create(
                related_user=user, defaults={"right_count": "0", "wrong_count": "1"}
            )
            if not created:
                record.wrong_count += 1
        record.save()
        return Response(
            {"msg": "record updated sucessfully"}, status=status.HTTP_200_OK
        )
