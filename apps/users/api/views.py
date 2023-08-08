from rest_framework import viewsets, permissions

from . import serializers
from ..models import User
from apps.auth.api.authentication import JWTCookieAuthentication

class UserViewset(viewsets.ModelViewSet):
  serializer_class = serializers.UserSerializer
  queryset = User.objects.all()
  permission_classes = [permissions.IsAuthenticated]
  authentication_classes = [JWTCookieAuthentication]
