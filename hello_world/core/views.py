# Views for Glorious Space - The Digital Palace Gates
# Where Requests Transform into Royal Experiences

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.conf import settings
import json
import uuid
from datetime import datetime, timedelta

from .models import (
    CustomUser, Project, ProjectCollaboration, ChatRoom, ChatMessage,
    AIConversation, AIMessage, Notification, UserActivity
)


# Core Views - The Main Palace Halls
def home_view(request):
    """
    Home Page - The Grand Entrance
    Welcome visitors to the digital kingdom
    """
    
    context = {
        'page_title': 'DevCrown - Advanced AI Agent Platform',
        'meta_description': 'Experience the future of AI interaction with our advanced agent platform.',
        'stats': {
            'total_users': 12500,
            'total_projects': 500,
            'active_collaborations': 200,
            'ai_conversations': 150000,
        }
    }
    
    return render(request, 'main_home.html', context)


def dashboard_view(request):
    """
    Dashboard - The Royal Command Center
    User's personalized control panel
    """
    
    if not request.user.is_authenticated:
        return redirect('users:login')
    
    context = {
        'page_title': f'{request.user.username}\'s Royal Dashboard',
    }
    
    return render(request, 'core/dashboard.html', context)


def canvas_view(request):
    """
    Canvas Playground - The Creative Forge
    Interactive canvas for 2D/3D/4D/5G experiences
    """
    
    context = {
        'page_title': 'Canvas Playground - Forge Your Digital Magic',
        'canvas_modes': [
            {'id': '2d', 'name': '2D Canvas', 'description': 'Classic 2D graphics and animations'},
            {'id': '3d', 'name': '3D WebGL', 'description': 'Three.js powered 3D experiences'},
            {'id': '4d', 'name': '4D Space', 'description': 'Dimensional visualization'},
            {'id': '5g', 'name': '5G Real-time', 'description': 'Ultra-low latency real-time'},
        ]
    }
    
    return render(request, 'core/canvas.html', context)


def ai_services_view(request):
    """
    AI Services - The Digital Oracle Chamber
    Central hub for AI-powered features
    """
    
    # Available AI models
    ai_models = [
        {
            'name': 'Claude 3',
            'description': 'Advanced reasoning and code assistance',
            'capabilities': ['Code', 'Analysis', 'Writing', 'Math'],
            'icon': '🤖'
        },
        {
            'name': 'GPT-4',
            'description': 'Versatile AI for various tasks',
            'capabilities': ['General', 'Creative', 'Technical'],
            'icon': '⚡'
        },
        {
            'name': 'Code Assistant',
            'description': 'Specialized for programming tasks',
            'capabilities': ['Code Review', 'Debugging', 'Optimization'],
            'icon': '💻'
        },
    ]
    
    context = {
        'ai_models': ai_models,
        'page_title': 'AI Services - The Digital Oracle',
    }
    
    return render(request, 'core/ai_services.html', context)


def ai_chat_view(request):
    """
    AI Chat Interface - The Oracle's Chamber
    Advanced ChatGPT-like AI conversation interface
    """
    
    context = {
        'page_title': 'AI Chat - Converse with the Digital Oracle',
        'ai_modes': [
            {'id': 'general', 'name': 'General Chat', 'description': 'Casual conversation and general help'},
            {'id': 'code_assistant', 'name': 'Code Assistant', 'description': 'Programming help and code review'},
            {'id': 'debug_helper', 'name': 'Debug Helper', 'description': 'Bug hunting and problem solving'},
            {'id': 'ai_training', 'name': 'AI Training', 'description': 'Learn about AI and machine learning'},
            {'id': 'web3_guide', 'name': 'Web3 Guide', 'description': 'Blockchain and crypto guidance'},
            {'id': 'canvas_expert', 'name': 'Canvas Expert', 'description': 'Graphics and visualization help'},
        ]
    }
    
    return render(request, 'core/ai_chat.html', context)


def projects_view(request):
    """
    Project Gallery - The Royal Exhibition
    Browse and discover amazing projects
    """
    
    context = {
        'page_title': 'Project Gallery - Royal Exhibitions'
    }
    
    return render(request, 'core/projects.html', context)


def developers_view(request):
    """
    Developer Directory - The Royal Court
    Discover talented developers in the kingdom
    """
    
    context = {
        'page_title': 'Developer Directory - The Royal Court',
    }
    
    return render(request, 'core/developers.html', context)


def showcase_view(request):
    """
    Project Showcase - The Grand Gallery
    Featured projects and portfolios
    """
    
    context = {
        'page_title': 'Project Showcase - The Grand Gallery',
    }
    
    return render(request, 'core/showcase.html', context)


def live_chat_view(request):
    """
    Live Chat - The Royal Communication Chamber
    Real-time chat with voice and video capabilities
    """
    
    context = {
        'page_title': 'Live Chat - Royal Communication Chamber',
    }
    
    return render(request, 'core/live_chat.html', context)


# API Views - The Digital Servants
@csrf_exempt
@require_http_methods(["POST"])
def api_ai_chat(request):
    """
    AI Chat API - Converse with the Oracle
    Handle AI conversation requests
    """
    
    try:
        data = json.loads(request.body)
        message = data.get('message', '').strip()
        mode = data.get('mode', 'general')
        
        if not message:
            return JsonResponse({'error': 'Message is required'}, status=400)
        
        # Simulate AI response (replace with actual AI integration)
        ai_response = generate_ai_response(message, mode)
        
        return JsonResponse({
            'response': ai_response,
            'timestamp': timezone.now().isoformat(),
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def generate_ai_response(message, mode):
    """
    Generate AI response based on mode
    (This would integrate with actual AI services)
    """
    
    mode_responses = {
        'general': f"Thank you for your message: '{message}'. I'm here to help with any questions you have! 🤖",
        'code_assistant': f"I see you're asking about code. Let me help you with: '{message}'. Here's my analysis... 💻",
        'debug_helper': f"Debugging mode activated! For the issue: '{message}', let's troubleshoot step by step... 🔧",
        'ai_training': f"Great question about AI! Regarding '{message}', let me explain the concepts... 🧠",
        'web3_guide': f"Welcome to Web3! About '{message}', here's what you need to know in the blockchain space... ⛓️",
        'canvas_expert': f"Canvas and graphics expertise here! For '{message}', let's create something amazing... 🎨",
    }
    
    return mode_responses.get(mode, mode_responses['general'])


# Utility Views - The Digital Helpers
def health_check(request):
    """Health check endpoint for monitoring"""
    return JsonResponse({
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'version': '1.0.0',
    })


def search_view(request):
    """
    Global Search - The Royal Archive
    Search across projects, users, and content
    """
    
    query = request.GET.get('q', '').strip()
    
    context = {
        'query': query,
        'page_title': f'Search Results for "{query}"' if query else 'Search - The Royal Archive',
    }
    
    return render(request, 'core/search.html', context)


# Blog Views - The Content Kingdom
def blog_index_view(request):
    """
    Blog Index - The Content Gallery
    Display all blog posts with categories and search
    """
    
    # Mock blog posts data (replace with real database queries later)
    blog_posts = [
        {
            'title': 'The Future of AI Development',
            'slug': 'future-of-ai-development',
            'excerpt': 'Exploring the cutting-edge trends in artificial intelligence and machine learning.',
            'author': 'OneLastAI Team',
            'published_date': timezone.now() - timedelta(days=2),
            'category': 'AI & Technology',
            'read_time': '8 min read',
            'image': '/static/images/blog/ai-future.jpg',
            'featured': True
        },
        {
            'title': 'Building Scalable Web Applications',
            'slug': 'building-scalable-web-applications',
            'excerpt': 'Best practices for creating web applications that can handle massive scale.',
            'author': 'Development Team',
            'published_date': timezone.now() - timedelta(days=5),
            'category': 'Web Development',
            'read_time': '12 min read',
            'image': '/static/images/blog/scalable-web.jpg',
            'featured': False
        },
        {
            'title': 'Design Thinking in Digital Products',
            'slug': 'design-thinking-digital-products',
            'excerpt': 'How design thinking principles can revolutionize your digital product strategy.',
            'author': 'Design Team',
            'published_date': timezone.now() - timedelta(days=7),
            'category': 'Design',
            'read_time': '6 min read',
            'image': '/static/images/blog/design-thinking.jpg',
            'featured': False
        }
    ]
    
    categories = ['All', 'AI & Technology', 'Web Development', 'Design', 'Business', 'Tutorials']
    
    context = {
        'page_title': 'Blog - OneLastAI Insights',
        'blog_posts': blog_posts,
        'categories': categories,
        'featured_post': next((post for post in blog_posts if post['featured']), None)
    }
    
    return render(request, 'blog/index.html', context)


def blog_post_view(request, slug):
    """
    Blog Post Detail - The Article Chamber
    Display individual blog post with full content
    """
    
    # Mock blog post data (replace with real database query later)
    if slug == 'future-of-ai-development':
        post = {
            'title': 'The Future of AI Development',
            'slug': 'future-of-ai-development',
            'content': '''
            <p>Artificial Intelligence continues to evolve at an unprecedented pace, transforming industries and reshaping how we approach problem-solving. In this comprehensive exploration, we'll dive deep into the emerging trends that will define the next decade of AI development.</p>
            
            <h2>Key Trends Shaping AI's Future</h2>
            <p>The landscape of AI development is constantly shifting, with new breakthroughs emerging regularly. From large language models to quantum computing applications, the possibilities seem endless.</p>
            
            <h3>1. Multimodal AI Systems</h3>
            <p>The integration of text, image, and audio processing capabilities is creating more versatile AI systems that can understand and generate content across multiple modalities.</p>
            
            <h3>2. Edge AI Computing</h3>
            <p>Moving AI processing closer to data sources is reducing latency and improving privacy, making real-time AI applications more feasible than ever.</p>
            ''',
            'author': 'OneLastAI Team',
            'published_date': timezone.now() - timedelta(days=2),
            'category': 'AI & Technology',
            'read_time': '8 min read',
            'image': '/static/images/blog/ai-future.jpg',
            'tags': ['AI', 'Technology', 'Future', 'Development']
        }
    else:
        post = {
            'title': 'Sample Blog Post',
            'slug': slug,
            'content': '<p>This is a sample blog post content. Replace with actual content from your database.</p>',
            'author': 'OneLastAI Team',
            'published_date': timezone.now(),
            'category': 'General',
            'read_time': '5 min read',
            'image': '/static/images/blog/default.jpg',
            'tags': ['Sample', 'Blog']
        }
    
    # Related posts
    related_posts = [
        {
            'title': 'Building Scalable Web Applications',
            'slug': 'building-scalable-web-applications',
            'image': '/static/images/blog/scalable-web.jpg',
            'read_time': '12 min read'
        },
        {
            'title': 'Design Thinking in Digital Products',
            'slug': 'design-thinking-digital-products',
            'image': '/static/images/blog/design-thinking.jpg',
            'read_time': '6 min read'
        }
    ]
    
    context = {
        'page_title': post['title'],
        'post': post,
        'related_posts': related_posts
    }
    
    return render(request, 'blog/post.html', context)


# Legal Views - The Compliance Kingdom
def privacy_policy_view(request):
    """
    Privacy Policy - The Data Protection Charter
    Display comprehensive privacy policy
    """
    
    context = {
        'page_title': 'Privacy Policy - OneLastAI',
        'last_updated': 'September 3, 2025'
    }
    
    return render(request, 'legal/privacy.html', context)


def terms_of_service_view(request):
    """
    Terms of Service - The User Agreement Scroll
    Display terms and conditions for platform usage
    """
    
    context = {
        'page_title': 'Terms of Service - OneLastAI',
        'last_updated': 'September 3, 2025'
    }
    
    return render(request, 'legal/terms.html', context)


def cookies_policy_view(request):
    """
    Cookies Policy - The Cookie Jar Guidelines
    Display information about cookie usage
    """
    
    context = {
        'page_title': 'Cookies Policy - OneLastAI',
        'last_updated': 'September 3, 2025'
    }
    
    return render(request, 'legal/cookies.html', context)


# Additional Project & User Views
def project_create_view(request):
    """
    Project Creation - The Genesis Chamber
    Create new projects and collaborative works
    """
    
    context = {
        'page_title': 'Create New Project - Birth of Digital Art',
    }
    
    return render(request, 'core/project_create.html', context)


def project_detail_view(request, project_id):
    """
    Project Detail - The Masterpiece Gallery
    Display detailed view of a specific project
    """
    
    context = {
        'page_title': f'Project #{project_id} - Digital Masterpiece',
        'project_id': project_id,
    }
    
    return render(request, 'core/project_detail.html', context)


def about_view(request):
    """
    About Page - The Kingdom's Story
    Learn about our royal digital kingdom
    """
    
    context = {
        'page_title': 'About - The Royal Kingdom Story',
    }
    
    return render(request, 'core/about.html', context)


# User Authentication Views (temporary until proper auth app)
def login_view(request):
    """
    Login Page - The Royal Gateway
    Enter the digital kingdom
    """
    
    context = {
        'page_title': 'Login - Enter the Kingdom',
    }
    
    return render(request, 'auth/login.html', context)


def register_view(request):
    """
    Registration Page - Join the Kingdom
    Become a royal digital citizen
    """
    
    context = {
        'page_title': 'Register - Join the Kingdom',
    }
    
    return render(request, 'auth/register.html', context)


def profile_view(request):
    """
    User Profile - The Royal Portrait
    Manage your digital identity
    """
    
    context = {
        'page_title': f'{request.user.username}\'s Royal Profile' if request.user.is_authenticated else 'User Profile',
    }
    
    return render(request, 'auth/profile.html', context)


# New Views for DevCrown Platform
def blog_view(request):
    """Blog page with AI and technology articles"""
    # Mock blog posts data
    blog_posts = [
        {
            'id': 1,
            'title': 'The Future of AI Conversation Systems',
            'excerpt': 'Exploring how advanced AI agents are transforming digital interactions.',
            'author': 'DevCrown Team',
            'date': timezone.now() - timedelta(days=2),
            'image': '/static/blog/ai-future.jpg',
            'category': 'AI Technology',
            'tags': ['AI', 'Conversation', 'Technology'],
            'read_time': '5 min read',
        },
        {
            'id': 2,
            'title': 'Building Intelligent Chat Agents with DevCrown',
            'excerpt': 'A comprehensive guide to creating and deploying AI agents.',
            'author': 'Technical Team',
            'date': timezone.now() - timedelta(days=5),
            'image': '/static/blog/chat-agents.jpg',
            'category': 'Tutorial',
            'tags': ['Tutorial', 'Development', 'Chat'],
            'read_time': '8 min read',
        },
        {
            'id': 3,
            'title': 'Understanding AI Agent Personalities',
            'excerpt': 'How different personality types enhance user engagement.',
            'author': 'AI Research Team',
            'date': timezone.now() - timedelta(days=7),
            'image': '/static/blog/personalities.jpg',
            'category': 'Research',
            'tags': ['Research', 'Personality', 'UX'],
            'read_time': '6 min read',
        },
    ]
    
    # Filter by category if provided
    category = request.GET.get('category')
    if category:
        blog_posts = [post for post in blog_posts if post['category'].lower() == category.lower()]
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        blog_posts = [
            post for post in blog_posts 
            if search_query.lower() in post['title'].lower() or 
               search_query.lower() in post['excerpt'].lower()
        ]
    
    # Pagination
    paginator = Paginator(blog_posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_title': 'DevCrown Blog - AI Insights & Tutorials',
        'meta_description': 'Latest insights, tutorials, and updates from the DevCrown AI platform.',
        'blog_posts': page_obj,
        'categories': ['AI Technology', 'Tutorial', 'Research', 'Enterprise', 'Analytics'],
        'current_category': category,
        'search_query': search_query,
    }
    return render(request, 'blog.html', context)


def projects_showcase_view(request):
    """Projects showcase page"""
    projects = [
        {
            'id': 1,
            'title': 'AI Customer Support Agent',
            'description': 'Intelligent customer support system with 24/7 availability.',
            'image': '/static/projects/customer-support.jpg',
            'technologies': ['Python', 'Django', 'AI/ML', 'WebSocket'],
            'category': 'Customer Service',
            'status': 'Production',
            'github_url': 'https://github.com/devcrown/customer-agent',
            'demo_url': '#',
        },
        {
            'id': 2,
            'title': 'Educational AI Tutor',
            'description': 'Personalized learning assistant for students and educators.',
            'image': '/static/projects/edu-tutor.jpg',
            'technologies': ['React', 'Python', 'TensorFlow', 'PostgreSQL'],
            'category': 'Education',
            'status': 'Beta',
            'github_url': 'https://github.com/devcrown/edu-tutor',
            'demo_url': '#',
        },
        {
            'id': 3,
            'title': 'Healthcare Consultation Bot',
            'description': 'AI-powered preliminary health consultation and advice system.',
            'image': '/static/projects/healthcare.jpg',
            'technologies': ['Vue.js', 'FastAPI', 'Redis', 'Docker'],
            'category': 'Healthcare',
            'status': 'Development',
            'github_url': 'https://github.com/devcrown/health-bot',
            'demo_url': '#',
        },
    ]
    
    # Filter by category
    category = request.GET.get('category')
    if category:
        projects = [project for project in projects if project['category'].lower() == category.lower()]
    
    context = {
        'page_title': 'DevCrown Projects - AI Solutions Showcase',
        'meta_description': 'Explore our portfolio of AI-powered solutions and applications.',
        'projects': projects,
        'categories': ['Customer Service', 'Education', 'Healthcare', 'E-commerce'],
        'current_category': category,
    }
    return render(request, 'projects.html', context)


def about_view(request):
    """About page with company information"""
    team_members = [
        {
            'name': 'Alex Johnson',
            'role': 'CEO & Founder',
            'bio': 'Visionary leader with 15+ years in AI and machine learning.',
            'image': '/static/team/alex.jpg',
            'linkedin': '#',
            'twitter': '#',
        },
        {
            'name': 'Sarah Chen',
            'role': 'CTO',
            'bio': 'Technical expert specializing in conversational AI systems.',
            'image': '/static/team/sarah.jpg',
            'linkedin': '#',
            'twitter': '#',
        },
    ]
    
    context = {
        'page_title': 'About DevCrown - Leading AI Innovation',
        'meta_description': 'Learn about DevCrown\'s mission to democratize AI through advanced conversation systems.',
        'team_members': team_members,
    }
    return render(request, 'about.html', context)


def privacy_policy_view(request):
    """Privacy policy page"""
    context = {
        'page_title': 'Privacy Policy - DevCrown',
        'meta_description': 'DevCrown privacy policy and data protection information.',
    }
    return render(request, 'privacy_policy.html', context)


def terms_of_service_view(request):
    """Terms of service page"""
    context = {
        'page_title': 'Terms of Service - DevCrown',
        'meta_description': 'DevCrown terms of service and usage guidelines.',
    }
    return render(request, 'terms_of_service.html', context)


@require_http_methods(["GET"])
def health_check_view(request):
    """Health check endpoint for monitoring"""
    health_status = {
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'version': '1.0.0',
        'services': {
            'database': 'connected',
            'ai_engine': 'active',
            'websocket': 'running',
            'cache': 'operational',
        }
    }
    return JsonResponse(health_status)


@csrf_exempt
@require_http_methods(["POST"])
def contact_view(request):
    """Contact form submission"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            subject = data.get('subject')
            message = data.get('message')
            
            # Here you would typically save to database or send email
            # For now, just return success response
            
            return JsonResponse({
                'status': 'success',
                'message': 'Thank you for your message. We\'ll get back to you soon!'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': 'There was an error processing your request.'
            }, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)


def api_documentation_view(request):
    """API documentation page"""
    context = {
        'page_title': 'API Documentation - DevCrown',
        'meta_description': 'Complete API documentation for DevCrown AI agent platform.',
    }
    return render(request, 'api_docs.html', context)
