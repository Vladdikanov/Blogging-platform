from rest_framework.routers import DefaultRouter
from .views import PostViewSet

router = DefaultRouter()
router.register(r'', PostViewSet, basename="post")
# router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = router.urls