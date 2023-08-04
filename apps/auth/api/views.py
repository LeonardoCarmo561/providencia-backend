from rest_framework import status, exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.conf import settings
from django.middleware import csrf
from django.utils.translation import gettext as _

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt import exceptions as jwt_exceptions
from rest_framework_simplejwt.views import (
    TokenObtainPairView as DefaultTokenObtainPairView,
    TokenRefreshView as DefaultTokenRefreshView
)

from apps.users.models import User

from .serializers import TokenObtainPairSerializer
from .authentication import JWTCookieAuthentication

class TokenObtainPairView(DefaultTokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = Response()
        serializer = self.get_serializer(data=request.data)
        email = serializer.initial_data['email']
        user = User.objects.filter(email = email).first()
        if user:
            pass
        else:
            raise exceptions.APIException(_('E-mail not registered'), status.HTTP_404_NOT_FOUND)

        try:
            serializer.is_valid(raise_exception=True)
        except jwt_exceptions.TokenError as e:
            raise jwt_exceptions.InvalidToken(e.args[0])

        data = serializer.validated_data
        response.set_cookie(
            value = data['access'],
            key = settings.SIMPLE_JWT['AUTH_COOKIE'],
            secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        )
        response.set_cookie(
            value = data['refresh'],
            key = settings.SIMPLE_JWT['REFRESH_COOKIE'],
            secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            expires = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        )
        csrf.get_token(request)
        response.data = {'Success':'Login bem Sucedido', 'data':serializer.validated_data}
        return response

class TokenRefreshPairView(DefaultTokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get(settings.SIMPLE_JWT['REFRESH_COOKIE'])
        request_data = {}
        request_data['refresh'] = refresh
        serializer = self.get_serializer(data=request_data)
        try:
            serializer.is_valid(raise_exception=True)
        except jwt_exceptions.TokenError as e:
            raise jwt_exceptions.InvalidToken(e.args[0])
        data = serializer.data
        response = Response()
        response.set_cookie(
            value = data['access'],
            key = settings.SIMPLE_JWT['AUTH_COOKIE'],
            secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        )
        response.set_cookie(
            value = data['refresh'],
            key = settings.SIMPLE_JWT['REFRESH_COOKIE'],
            secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            expires = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        )
        csrf.get_token(request)
        response.data = {'access': data['access'], 'refresh': data['refresh']}
        
        return response

class TokenLogoutView(APIView):
    http_method_names = ['post']
    authentication_classes = [JWTCookieAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_cookie = request.COOKIES.get(settings.SIMPLE_JWT['REFRESH_COOKIE'])
            refresh = RefreshToken(refresh_cookie)
            refresh.blacklist()
            response = Response()
            response.delete_cookie(settings.SIMPLE_JWT['REFRESH_COOKIE'])
            response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
            response.data = {'Success':'Deslogado com suceso'}
            response.status_code = status.HTTP_205_RESET_CONTENT
            return response

        except Exception as e:
            raise Response(status = status.HTTP_400_BAD_REQUEST)

