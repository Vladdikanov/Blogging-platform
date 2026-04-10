from rest_framework import viewsets, permissions
from django.db.models import Count
from .models import Post, Comment
from .filters import PostFilter
from .serializers import PostSerializer, CommentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter



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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]

    filterset_class = PostFilter
    ordering_fields = ['created_at', "title", "likes_count", "comments_count"]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if user in post.likes.all():
            return Response({'detail': 'Уже лайкнул'}, status=400)

        post.likes.add(user)
        return Response({'detail': 'Лайк поставлен'})
    
    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if user not in post.likes.all():
            return Response({'detail': 'Лайка нет'}, status=400)

        post.likes.remove(user)
        return Response({'detail': 'Лайк убран'})
    
    @action(detail=True, methods=['post'])
    def comments(self, request, pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
