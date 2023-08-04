from django.urls import path

from .views import (
    TokenLogoutView,
    TokenObtainPairView,
    TokenRefreshPairView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair_view'),
    path('token/refresh/', TokenRefreshPairView.as_view(), name='token_refresh_pair_view'),
    path('token/logout/', TokenLogoutView.as_view(), name='token_logout_view')
]
