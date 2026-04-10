from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'updated_at']
        read_only_fields = ['post', 'author']

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    likes_count = serializers.SerializerMethodField()
    likes = serializers.SlugRelatedField(many=True, read_only=True, slug_field='email')
    is_liked = serializers.SerializerMethodField()
    author_id = serializers.ReadOnlyField(source='author.id')
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return user in obj.likes.all()
    
    def get_comments_count(self, obj):
        return obj.comments.count()

