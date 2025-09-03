from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Project, CanvasSession, CodeSnippet, TechStack, Collaboration
from backend.apps.users.models import CustomUser


def home(request):
    """Home page with featured content"""
    featured_projects = Project.objects.filter(featured=True, is_public=True)[:6]
    latest_projects = Project.objects.filter(is_public=True)[:8]
    active_developers = CustomUser.objects.filter(is_developer=True, is_active=True)[:12]
    tech_stacks = TechStack.objects.order_by('-popularity_score')[:10]
    
    context = {
        'featured_projects': featured_projects,
        'latest_projects': latest_projects,
        'active_developers': active_developers,
        'tech_stacks': tech_stacks,
        'total_developers': CustomUser.objects.filter(is_developer=True).count(),
        'total_projects': Project.objects.filter(is_public=True).count(),
    }
    
    return render(request, 'core/home.html', context)


@login_required
def dashboard(request):
    """Developer dashboard"""
    user = request.user
    user_projects = Project.objects.filter(owner=user)[:5]
    user_sessions = CanvasSession.objects.filter(user=user)[:5]
    recent_snippets = CodeSnippet.objects.filter(author=user)[:5]
    
    # Get collaboration invitations
    collaborations = Collaboration.objects.filter(
        participants=user, is_active=True
    )[:5]
    
    context = {
        'user_projects': user_projects,
        'user_sessions': user_sessions,
        'recent_snippets': recent_snippets,
        'collaborations': collaborations,
    }
    
    return render(request, 'core/dashboard.html', context)


def projects_list(request):
    """List all public projects"""
    projects = Project.objects.filter(is_public=True)
    
    # Filter by technology
    tech_filter = request.GET.get('tech')
    if tech_filter:
        projects = projects.filter(technologies__icontains=tech_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        projects = projects.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(technologies__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(projects, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get available technologies for filter
    all_projects = Project.objects.filter(is_public=True)
    technologies = set()
    for project in all_projects:
        technologies.update(project.technologies)
    
    context = {
        'page_obj': page_obj,
        'technologies': sorted(technologies),
        'current_tech': tech_filter,
        'search_query': search_query,
    }
    
    return render(request, 'core/projects.html', context)


def project_detail(request, project_id):
    """Project detail view"""
    project = get_object_or_404(Project, id=project_id, is_public=True)
    
    # Increment view count
    project.views_count += 1
    project.save()
    
    # Get related projects
    related_projects = Project.objects.filter(
        is_public=True,
        technologies__overlap=project.technologies
    ).exclude(id=project.id)[:4]
    
    context = {
        'project': project,
        'related_projects': related_projects,
    }
    
    return render(request, 'core/project_detail.html', context)


def developers_list(request):
    """List all developers"""
    developers = CustomUser.objects.filter(is_developer=True, is_active=True)
    
    # Filter by experience level
    experience_filter = request.GET.get('experience')
    if experience_filter:
        developers = developers.filter(developer_profile__experience_level=experience_filter)
    
    # Filter by skills
    skill_filter = request.GET.get('skill')
    if skill_filter:
        developers = developers.filter(skills__icontains=skill_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        developers = developers.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(bio__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(developers, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'experience_levels': ['junior', 'mid', 'senior', 'lead', 'architect'],
        'current_experience': experience_filter,
        'current_skill': skill_filter,
        'search_query': search_query,
    }
    
    return render(request, 'core/developers.html', context)


def canvas_playground(request):
    """Canvas playground for 2D/3D/4D rendering"""
    canvas_type = request.GET.get('type', '2d')
    
    if request.user.is_authenticated:
        user_sessions = CanvasSession.objects.filter(user=request.user, canvas_type=canvas_type)[:5]
    else:
        user_sessions = []
    
    public_sessions = CanvasSession.objects.filter(is_public=True, canvas_type=canvas_type)[:10]
    
    context = {
        'canvas_type': canvas_type,
        'user_sessions': user_sessions,
        'public_sessions': public_sessions,
    }
    
    template_map = {
        '2d': 'canvas/canvas_2d.html',
        '3d': 'canvas/canvas_3d.html',
        '4d': 'canvas/canvas_4d.html',
        '5g': 'canvas/canvas_5g.html',
    }
    
    template = template_map.get(canvas_type, 'canvas/canvas_2d.html')
    return render(request, template, context)


@login_required
def create_project(request):
    """Create new project"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        technologies = request.POST.get('technologies', '').split(',')
        github_url = request.POST.get('github_url')
        demo_url = request.POST.get('demo_url')
        is_public = request.POST.get('is_public') == 'on'
        
        project = Project.objects.create(
            name=name,
            description=description,
            owner=request.user,
            technologies=[tech.strip() for tech in technologies if tech.strip()],
            github_url=github_url,
            demo_url=demo_url,
            is_public=is_public
        )
        
        messages.success(request, f'Project "{name}" created successfully!')
        return redirect('core:project_detail', project_id=project.id)
    
    return render(request, 'core/create_project.html')


def about(request):
    """About page"""
    stats = {
        'total_developers': CustomUser.objects.filter(is_developer=True).count(),
        'total_projects': Project.objects.filter(is_public=True).count(),
        'total_canvas_sessions': CanvasSession.objects.filter(is_public=True).count(),
        'total_collaborations': Collaboration.objects.filter(is_active=True).count(),
    }
    
    context = {'stats': stats}
    return render(request, 'core/about.html', context)
