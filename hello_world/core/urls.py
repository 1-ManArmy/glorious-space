# URL Routing for Glorious Space - The Royal Navigation
# Where Every Path Leads to Digital Magnificence

from django.urls import path, include
from . import views

app_name = 'core'

urlpatterns = [
    # Core Palace Routes
    path('', views.home_view, name='index'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # New Pages
    path('blog/', views.blog_view, name='blog'),
    path('projects/', views.projects_showcase_view, name='projects'),
    path('about/', views.about_view, name='about'),
    path('privacy-policy/', views.privacy_policy_view, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service_view, name='terms_of_service'),
    path('health/', views.health_check_view, name='health_check'),
    path('contact/', views.contact_view, name='contact'),
    path('api-docs/', views.api_documentation_view, name='api_docs'),
    
    # Creative & Technical Chambers
    path('canvas/', views.canvas_view, name='canvas'),
    path('canvas/playground/', views.canvas_view, name='canvas_playground'),
    path('ai-services/', views.ai_services_view, name='ai_services'),
    path('ai-chat/', views.ai_chat_view, name='ai_chat'),
    
    # Original Project & Community Routes
    path('old-projects/', views.projects_view, name='old_projects'),
    path('projects/create/', views.project_create_view, name='project_create'),
    path('projects/<int:project_id>/', views.project_detail_view, name='project_detail'),
    path('developers/', views.developers_view, name='developers'),
    path('showcase/', views.showcase_view, name='showcase'),
    path('live-chat/', views.live_chat_view, name='live_chat'),
    
    # Search & Discovery
    path('search/', views.search_view, name='search'),
    
    # Blog & Content Routes
    path('blog/', views.blog_index_view, name='blog'),
    path('blog/<slug:slug>/', views.blog_post_view, name='blog_post'),
    
    # Legal & Compliance Routes
    path('legal/privacy/', views.privacy_policy_view, name='privacy_policy'),
    path('legal/terms/', views.terms_of_service_view, name='terms_of_service'),
    path('legal/cookies/', views.cookies_policy_view, name='cookies_policy'),
    
    # User Authentication Routes (temporary)
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('about/', views.about_view, name='about'),
    
    # API Endpoints - The Digital Servants
    path('api/ai-chat/', views.api_ai_chat, name='api_ai_chat'),
    
    # Health & Monitoring
    path('health/', views.health_check, name='health_check'),
]
