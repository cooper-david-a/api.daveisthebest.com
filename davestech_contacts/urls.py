from rest_framework import routers
from .views import ContactViewSet

router = routers.DefaultRouter()
router.register("", ContactViewSet, basename="contacts")

urlpatterns = router.urls