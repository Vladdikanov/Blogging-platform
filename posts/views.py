from rest_framework import viewsets, permissions
from django.db.models import Count
from .models import Post, Comment
from .filters import PostFilter
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer, CommentSerializer, EmptySerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
# from drf_yasg.utils import swagger_auto_schema, no_body
# from drf_yasg import openapi

@extend_schema_view(
    list=extend_schema(
        description="Получить список постов с фильтрацией, поиском и сортировкой",
        parameters=[
            OpenApiParameter(
                name='author',
                description='Фильтр по ID автора',
                required=False,
                type=OpenApiTypes.INT,
            ),
            OpenApiParameter(
                name='created_date',
                description='Фильтр по дате создания (YYYY-MM-DD)',
                required=False,
                type=OpenApiTypes.DATE,
            ),
            OpenApiParameter(
                name='created_after',
                description='Посты после даты (YYYY-MM-DD)',
                required=False,
                type=OpenApiTypes.DATE,
            ),
            OpenApiParameter(
                name='created_before',
                description='Посты до даты (YYYY-MM-DD)',
                required=False,
                type=OpenApiTypes.DATE,
            ),
            OpenApiParameter(
                name='ordering',
                description='Сортировка: created_at, -created_at, title, -title, likes_count, -likes_count, comments_count, -comments_count',
                required=False,
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name='search',
                description='Поиск по заголовку и содержимому',
                required=False,
                type=OpenApiTypes.STR,
            ),
        ],
        responses={
            200: PostSerializer(many=True),
        }
    ),
    create=extend_schema(
        description="Создать новый пост. Автор определяется автоматически.",
        request=PostSerializer,
        responses={
            201: PostSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            401: OpenApiResponse(description="Не авторизован"),
        },
        examples=[
            OpenApiExample(
                "Пример запроса",
                value={"title": "Мой пост", "content": "Содержание поста"},
                request_only=True,
            ),
        ],
    ),
    retrieve=extend_schema(
        description="Получить конкретный пост по ID",
        responses={
            200: PostSerializer,
            404: OpenApiResponse(description="Пост не найден"),
        }
    ),
    update=extend_schema(
        description="Полностью обновить пост (только для автора)",
        request=PostSerializer,
        responses={
            200: PostSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            401: OpenApiResponse(description="Не авторизован"),
            403: OpenApiResponse(description="Не автор поста"),
            404: OpenApiResponse(description="Пост не найден"),
        }
    ),
    partial_update=extend_schema(
        description="Частично обновить пост (только для автора)",
        request=PostSerializer,
        responses={
            200: PostSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            401: OpenApiResponse(description="Не авторизован"),
            403: OpenApiResponse(description="Не автор поста"),
            404: OpenApiResponse(description="Пост не найден"),
        }
    ),
    destroy=extend_schema(
        description="Удалить пост (только для автора)",
        responses={
            204: OpenApiResponse(description="Пост удалён"),
            401: OpenApiResponse(description="Не авторизован"),
            403: OpenApiResponse(description="Не автор поста"),
            404: OpenApiResponse(description="Пост не найден"),
        }
    ),
)
class PostViewSet(viewsets.ModelViewSet):
    # queryset = Post.objects.all().order_by('-created_at')

    def get_queryset(self):
        return Post.objects.annotate(
            likes_count=Count('likes'),
            comments_count=Count('comments')
        ).prefetch_related(
            'likes',          
            'comments',       
            'comments__author').order_by('-created_at')
    
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]

    filterset_class = PostFilter
    ordering_fields = ['created_at', "title", "likes_count", "comments_count"]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @extend_schema(
        description="Поставить лайк посту",
        request=None,
        responses={
            200: OpenApiResponse(description="Лайк поставлен"),
            400: OpenApiResponse(description="Уже лайкнул"),
            401: OpenApiResponse(description="Не авторизован"),
            404: OpenApiResponse(description="Пост не найден"),
        }
    )
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if user in post.likes.all():
            return Response({'detail': 'Уже лайкнул'}, status=400)

        post.likes.add(user)
        return Response({'detail': 'Лайк поставлен'})
    
    @extend_schema(
        description="Убрать лайк с поста",
        request=None,
        responses={
            200: OpenApiResponse(description="Лайк убран"),
            400: OpenApiResponse(description="Лайка нет"),
            401: OpenApiResponse(description="Не авторизован"),
            404: OpenApiResponse(description="Пост не найден"),
        }
    )
    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if user not in post.likes.all():
            return Response({'detail': 'Лайка нет'}, status=400)

        post.likes.remove(user)
        return Response({'detail': 'Лайк убран'})
    
    @extend_schema(
        description="Добавить комментарий к посту",
        request=CommentSerializer,
        responses={
            201: CommentSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            401: OpenApiResponse(description="Не авторизован"),
            404: OpenApiResponse(description="Пост не найден"),
        }
    )
    @action(detail=True, methods=['post'])
    def comments(self, request, pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
