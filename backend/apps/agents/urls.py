"""
Advanced URL routing for AI Agent Management System
Professional API endpoints and web interfaces
"""

from django.urls import path, include
from . import views

app_name = 'agents'

urlpatterns = [
    # Web Interface URLs
    path('', views.AgentDashboardView.as_view(), name='dashboard'),
    path('profile/<int:agent_id>/', views.AgentProfileView.as_view(), name='agent_profile'),
    path('training/', views.agent_training_view, name='training'),
    
    # API Endpoints
    path('api/', include([
        # Core Agent APIs
        path('chat/', views.AgentChatAPI.as_view(), name='chat_api'),
        path('list/', views.agent_list_api, name='agent_list_api'),
        path('analytics/<int:agent_id>/', views.agent_analytics_api, name='analytics_api'),
        path('feedback/', views.agent_feedback_api, name='feedback_api'),
        
        # Advanced Feature APIs
        path('capabilities/<int:agent_id>/', views.agent_capabilities_api, name='capabilities_api'),
        path('learning/<int:agent_id>/', views.agent_learning_api, name='learning_api'),
        path('memory/<int:agent_id>/', views.agent_memory_api, name='memory_api'),
        path('recommendations/<int:user_id>/', views.agent_recommendations_api, name='recommendations_api'),
        
        # Real-time Features
        path('status/', views.agent_status_api, name='status_api'),
        path('health-check/', views.agent_health_check, name='health_check'),
        path('performance/', views.performance_metrics_api, name='performance_api'),
    ])),
    
    # WebSocket endpoints for real-time chat
    # path('ws/chat/<str:agent_type>/', views.ChatConsumer.as_asgi(), name='chat_websocket'),
]
