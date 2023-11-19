from rest_framework import routers
from .views import CommentsViewSet

router = routers.DefaultRouter()
router.register("", CommentsViewSet, basename="comments")

urlpatterns = router.urls
