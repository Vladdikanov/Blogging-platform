from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser должен иметь is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser должен иметь is_superuser=True')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, 
                              verbose_name='Электронная почта', 
                              error_messages={
                                  'unique': 'Пользователь с такой почтой уже существует',
                                  'invalid': 'Введите корректный адрес электронной почты',
                                  })
    
    avatar_url = models.URLField(blank=True, 
                                 null=True,
                                 verbose_name='Ссылка на аватар')
    
    provider = models.CharField(max_length=50, 
                                blank=True, 
                                null=True,
                                verbose_name='Провайдер',
                                help_text='Через какой сервис авторизовался пользователь')
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email