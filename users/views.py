from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, GoogleAuthSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
# from drf_yasg.utils import swagger_auto_schema

class RegisterView(APIView):
    # @swagger_auto_schema(request_body=RegisterSerializer)
    @extend_schema(
        description="Регистрация нового пользователя по email и паролю",
        request=RegisterSerializer,
        responses={
            201: OpenApiResponse(
                response={
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                },
                description="Пользователь успешно создан"
            ),
            400: OpenApiResponse(description="Ошибка валидации"),
        },
        examples=[
            OpenApiExample(
                "Пример запроса",
                value={
                    "email": "user@example.com",
                    "password": "secure_password_123"
                },
                request_only=True,
            ),
            OpenApiExample(
                "Пример ответа",
                value={"message": "Пользователь создан"},
                response_only=True,
            ),
        ],
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Пользователь создан'}, status=201)

        return Response(serializer.errors, status=400)

class LoginView(APIView):
    # @swagger_auto_schema(request_body=LoginSerializer)
    @extend_schema(
        description="Вход по email и паролю. Возвращает JWT токены.",
        request=LoginSerializer,
        responses={
            200: OpenApiResponse(
                response={
                    'type': 'object',
                    'properties': {
                        'access': {'type': 'string', 'description': 'Access токен (JWT)'},
                        'refresh': {'type': 'string', 'description': 'Refresh токен (JWT)'}
                    }
                },
                description="Успешный вход"
            ),
            400: OpenApiResponse(description="Неверные учетные данные"),
        },
        examples=[
            OpenApiExample(
                "Пример запроса",
                value={
                    "email": "user@example.com",
                    "password": "secure_password_123"
                },
                request_only=True,
            ),
            OpenApiExample(
                "Пример ответа",
                value={
                    "access": "eyJhbGciOiJIUzI1NiIs...",
                    "refresh": "eyJhbGciOiJIUzI1NiIs..."
                },
                response_only=True,
            ),
        ],
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data

            refresh = RefreshToken.for_user(user)

            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            })

        return Response(serializer.errors, status=400)

class GoogleAuthView(APIView):
    # @swagger_auto_schema(request_body=GoogleAuthSerializer)
    @extend_schema(
        description="Вход через Google OAuth. Отправьте ID Token от Google.",
        request=GoogleAuthSerializer,
        responses={
            200: OpenApiResponse(
                response={
                    'type': 'object',
                    'properties': {
                        'access': {'type': 'string', 'description': 'Access токен (JWT)'},
                        'refresh': {'type': 'string', 'description': 'Refresh токен (JWT)'}
                    }
                },
                description="Успешный вход через Google"
            ),
            400: OpenApiResponse(description="Неверный токен Google"),
        },
        examples=[
            OpenApiExample(
                "Пример запроса",
                value={"token": "eyJhbGciOiJSUzI1NiIsImtpZCI6..."},
                request_only=True,
            ),
            OpenApiExample(
                "Пример ответа",
                value={
                    "access": "eyJhbGciOiJIUzI1NiIs...",
                    "refresh": "eyJhbGciOiJIUzI1NiIs..."
                },
                response_only=True,
            ),
        ],
    )
    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data

            refresh = RefreshToken.for_user(user)

            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            })

        return Response(serializer.errors, status=400)
