# URL Routes for Core Application - The Heart of Glorious Space
# Where Digital Dreams Come to Life

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # ============================================================================
    # MAIN NAVIGATION ROUTES - The Royal Pathways
    # ============================================================================
    
    # Homepage - The Grand Entrance
    path('', views.home, name='home'),
    
    # Dashboard - Command Center for Developers
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # ============================================================================
    # CREATIVE WORKSPACES - Where Magic Happens
    # ============================================================================
    
    # Canvas Playground - 2D/3D/4D/5G Graphics Laboratory
    path('canvas/', views.canvas_playground, name='canvas_playground'),
    
    # AI Chat Interface - ChatGPT-like Assistant
    path('ai-chat/', views.ai_chat, name='ai_chat'),
    
    # AI Services Marketplace - Intelligence as a Service
    path('ai-services/', views.ai_services, name='ai_services'),
    
    # ============================================================================
    # COMMUNITY & COLLABORATION - The Developer Kingdom
    # ============================================================================
    
    # Project Showcase - Gallery of Masterpieces
    path('showcase/', views.showcase, name='showcase'),
    
    # Developer Community - Networking & Collaboration
    path('developers/', views.developers_list, name='developers'),
    
    # Live Chat System - Real-time Communication
    path('live-chat/', views.live_chat, name='live_chat'),
    
    # ============================================================================
    # PROJECT MANAGEMENT - Build & Deploy Excellence
    # ============================================================================
    
    # Projects Gallery - User's Creative Portfolio
    path('projects/', views.projects_list, name='projects'),
    
    # Project Details - Deep Dive into Creations
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    
    # Project Creation & Editing
    path('projects/create/', views.create_project, name='create_project'),
    path('projects/<int:project_id>/edit/', views.edit_project, name='edit_project'),
    
    # ============================================================================
    # UTILITY ROUTES - Supporting Features
    # ============================================================================
    
    # About Page - Our Story
    path('about/', views.about, name='about'),
    
    # Contact & Support
    path('contact/', views.contact, name='contact'),
    
    # Help & FAQ
    path('help/', views.help, name='help'),
]
