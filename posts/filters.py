import django_filters
from .models import Post


class PostFilter(django_filters.FilterSet):

    author = django_filters.NumberFilter(field_name='author__id')

    created_date = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='date'
    )
    
    created_after = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gte'
    )
    created_before = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='lte'
    )

    class Meta:
        model = Post
        fields = []