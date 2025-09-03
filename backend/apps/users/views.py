from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import requests
import json
from keycloak.keycloak import KeycloakAuth
from .models import CustomUser, DeveloperProfile


def login_view(request):
    """Login view with Keycloak integration"""
    if request.method == 'POST':
        # Handle Keycloak OAuth login
        keycloak_auth = KeycloakAuth()
        redirect_url = keycloak_auth.get_login_url()
        return redirect(redirect_url)
    
    return render(request, 'users/login.html')


def logout_view(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('core:home')


@login_required
def profile_view(request):
    """User profile view"""
    profile, created = DeveloperProfile.objects.get_or_create(user=request.user)
    
    context = {
        'user': request.user,
        'profile': profile,
        'skills': request.user.skills,
        'projects': profile.portfolio_projects
    }
    
    return render(request, 'users/profile.html', context)


@login_required
@csrf_exempt
def update_profile(request):
    """API endpoint to update user profile"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = request.user
            profile = user.developer_profile
            
            # Update user fields
            if 'bio' in data:
                user.bio = data['bio']
            if 'skills' in data:
                user.skills = data['skills']
            if 'github_username' in data:
                user.github_username = data['github_username']
            if 'linkedin_profile' in data:
                user.linkedin_profile = data['linkedin_profile']
            if 'website' in data:
                user.website = data['website']
                
            user.save()
            
            # Update profile fields
            if 'experience_level' in data:
                profile.experience_level = data['experience_level']
            if 'specializations' in data:
                profile.specializations = data['specializations']
            if 'canvas_preferences' in data:
                profile.canvas_preferences = data['canvas_preferences']
                
            profile.save()
            
            return JsonResponse({'status': 'success', 'message': 'Profile updated successfully'})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def keycloak_callback(request):
    """Handle Keycloak OAuth callback"""
    try:
        keycloak_auth = KeycloakAuth()
        user_info = keycloak_auth.handle_callback(request)
        
        if user_info:
            # Create or get user
            user, created = CustomUser.objects.get_or_create(
                keycloak_id=user_info['sub'],
                defaults={
                    'username': user_info.get('preferred_username', user_info['email']),
                    'email': user_info['email'],
                    'first_name': user_info.get('given_name', ''),
                    'last_name': user_info.get('family_name', ''),
                }
            )
            
            # Create developer profile if it doesn't exist
            DeveloperProfile.objects.get_or_create(user=user)
            
            login(request, user)
            messages.success(request, 'Welcome to the Developer Crown Site!')
            return redirect('core:dashboard')
        else:
            messages.error(request, 'Authentication failed. Please try again.')
            return redirect('users:login')
            
    except Exception as e:
        messages.error(request, f'Authentication error: {str(e)}')
        return redirect('users:login')
