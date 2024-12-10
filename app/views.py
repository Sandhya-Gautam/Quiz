import random

from django.contrib.auth import authenticate
from django.core.cache import cache
from django.core.mail import BadHeaderError,send_mail
from django.conf  import settings
from django_q.tasks import async_task, result
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import Throttled
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView

from .models import Answers, Questions, Records
from .serializers import (
    QuestionSerializer,
    UserLoginSerializer,
    UserRegistrationSerializer,
)
from .task import calculate


class UserLogin(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def post(self, request):
        try:
            serializer = UserLoginSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.data.get("email")
                password = serializer.validated_data.get("password")
                user = authenticate(email=email, password=password)
                if user:
                    value = cache.get("testing")
                    subject='login alert'
                    message='A new login detected'
                    sender=settings.EMAIL_HOST_USER
                    try:
                        send_mail(subject,message,sender, [email])
                    except BadHeaderError:
                        return Response('mail sending error')
                    token, _created = Token.objects.get_or_create(user=user)
                    return Response(
                        {
                            "msg": "user login sucessful",
                            "token": token.key,
                            "cache_value": value,
                        },
                        status=status.HTTP_200_OK,
                    )
                return Response(
                    {"msg": "authentication error"}, status=status.HTTP_400_BAD_REQUEST
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Throttled as e:
            return Response({"error": "request limit exceeded", "default": e})


class UserRegister(APIView):
    throttle_classes= [UserRateThrottle, AnonRateThrottle]

    def post(self, request):
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"msg": "user registered sucessfully"}, status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Throttled:
            return Response({'error':'request limit exceeded'})

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

            # implementing django_q task

            task_id = async_task(calculate)
            task_response = result(task_id)

            # implementing cache
            cache.set("testing", "ramdom testing", timeout=60 * 10)

            return Response(
                {
                    "question": question.question,
                    "answers": serializer.data,
                    "task_response": task_response,
                },
                status=status.HTTP_200_OK,
            )
        except Answers.DoesNotExist:
            return Response(
                {"error": "No answer found for the selected question"},
                status=status.HTTP_404_NOT_FOUND,
            )


class CheckAnswer(APIView):
    permission_classes([permissions.IsAuthenticated])

    def put(self, request):
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

class GetScore(APIView):
    def get(self,request):
        user=request.user
        record=Records.objects.get(related_user=user)
        return Response({'right_count':record.right_count,'wrong_count':record.wrong_count})