from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('api/update-profile/', views.update_profile, name='update_profile'),
    path('keycloak/callback/', views.keycloak_callback, name='keycloak_callback'),
]
