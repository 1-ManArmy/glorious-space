# URL Routing for Glorious Space - The Royal Navigation
# Where Every Path Leads to Digital Magnificence

from django.urls import path, include
from . import views

app_name = 'core'

urlpatterns = [
    # Core Palace Routes
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Creative & Technical Chambers
    path('canvas/', views.canvas_view, name='canvas'),
    path('ai-services/', views.ai_services_view, name='ai_services'),
    path('ai-chat/', views.ai_chat_view, name='ai_chat'),
    
    # Project & Community Routes
    path('projects/', views.projects_view, name='projects'),
    path('developers/', views.developers_view, name='developers'),
    path('showcase/', views.showcase_view, name='showcase'),
    path('live-chat/', views.live_chat_view, name='live_chat'),
    
    # Search & Discovery
    path('search/', views.search_view, name='search'),
    
    # API Endpoints - The Digital Servants
    path('api/ai-chat/', views.api_ai_chat, name='api_ai_chat'),
    
    # Health & Monitoring
    path('health/', views.health_check, name='health_check'),
]
