from rest_framework_simplejwt.views import (
    TokenObtainPairView as BaseTokenObtainPairView,
    TokenRefreshView as BaseTokenRefreshView,
)

from .serializers import TokenObtainPairSerializer, TokenRefreshSerializer


class TokenObtainPairView(BaseTokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class TokenRefreshView(BaseTokenRefreshView):
    serializer_class = TokenRefreshSerializer
