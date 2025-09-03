# 👑 Keycloak Authentication URLs - Royal Gateway Routes
# URL patterns for Keycloak authentication flows

from django.urls import path
from .keycloak_views import (
    KeycloakLoginView,
    KeycloakTokenLoginView,
    keycloak_logout_view,
    refresh_token_view,
    KeycloakRegisterView,
    user_profile_view,
    keycloak_status_view,
    keycloak_callback_view,
)

app_name = 'auth'

urlpatterns = [
    # Keycloak Authentication Routes
    path('login/', KeycloakLoginView.as_view(), name='keycloak_login'),
    path('logout/', keycloak_logout_view, name='keycloak_logout'),
    path('register/', KeycloakRegisterView.as_view(), name='keycloak_register'),
    path('profile/', user_profile_view, name='profile'),
    
    # API Endpoints
    path('api/token/login/', KeycloakTokenLoginView.as_view(), name='token_login'),
    path('api/token/refresh/', refresh_token_view, name='refresh_token'),
    path('api/status/', keycloak_status_view, name='keycloak_status'),
    
    # OAuth Callback
    path('callback/', keycloak_callback_view, name='keycloak_callback'),
]
