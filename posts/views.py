from rest_framework import viewsets, permissions
from .models import Post
from .serializers import PostSerializer
from rest_framework.decorators import action
from rest_framework.response import Response



class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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
