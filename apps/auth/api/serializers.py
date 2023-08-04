from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as DefaultJWTTokenSerializer
from rest_framework_simplejwt import exceptions

from django.utils.translation import gettext as _

class TokenObtainPairSerializer(DefaultJWTTokenSerializer):
    @classmethod
    def get_token(cls, user):
        if user.is_active:
            token = super().get_token(user)

            token['email'] = user.email
            token['number'] = user.number
            token['is_superuser'] = user.is_superuser
            token['username'] = user.username

            return token
        else:
            raise exceptions.AuthenticationFailed(_('Inactive user'), 401)
