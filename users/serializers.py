from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(
            email=data['email'],
            password=data['password']
        )

        if not user:
            raise AuthenticationFailed('Неверные данные')

        if not user.is_active:
            raise AuthenticationFailed('Пользователь не активен')

        return user
    
class GoogleAuthSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, data):
        token = data.get('token')

        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )
        except ValueError as e:
            raise serializers.ValidationError(f'Неверный токен Google: {e}')

        email = idinfo.get('email')
        picture = idinfo.get('picture', '')

        if not email:
            raise serializers.ValidationError('Google не вернул email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_user(
                email=email,
                password=None,
                avatar_url=picture,
                provider='google',
            )

        return user