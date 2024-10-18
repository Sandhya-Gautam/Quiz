from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None,re_entered_password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be provided')
        if not username:
            raise ValueError('Username must be provided')
        if  password != re_entered_password:
            raise ValueError("Two password didnt match")
        
        user=self.model(
            email=email,
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, name, password=None):
        user = self.create_user(
            email,
            password=password,
            name=name
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

        


class User(AbstractUser):
    email=models.EmailField(unique=True)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']
    objects=UserManager()

    def __str__(self):
        return self.email

class Records(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    right_count=models.IntegerField()
    wrong_count=models.IntegerField()

class  Questions(models.Model):
    question=models.CharField(max_length=500, unique=True, primary_key=True)

class Answers(models.Model):
    question=models.ForeignKey(Questions, on_delete=models.CASCADE)
    answer=models.CharField(max_length=500)
    label=models.BooleanField()







