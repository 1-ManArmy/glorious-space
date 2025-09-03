from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'profiles', views.DeveloperProfileViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'canvas-sessions', views.CanvasSessionViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', views.dashboard_data, name='dashboard_data'),
    path('canvas/save/', views.save_canvas_data, name='save_canvas_data'),
]
