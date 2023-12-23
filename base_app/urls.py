from django.urls import path
from .views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt import views as simplejwt_views

#custom views to add expiration to serializers
urlpatterns = [
    path("jwt/create/", TokenObtainPairView.as_view(), name="jwt-create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", simplejwt_views.TokenVerifyView.as_view(), name="jwt-verify"),
]
