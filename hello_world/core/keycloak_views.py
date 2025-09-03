# 👑 Keycloak Authentication Views - Royal Login Portal
# Handles Keycloak authentication flows

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
import json
import logging

from .keycloak_auth import (
    refresh_keycloak_token,
    logout_keycloak_user,
    create_keycloak_user,
    get_keycloak_admin
)

logger = logging.getLogger(__name__)


class KeycloakLoginView(View):
    """
    Handle Keycloak login flow
    """
    template_name = 'auth/keycloak_login.html'
    
    def get(self, request):
        """
        Display login form or redirect if already authenticated
        """
        if request.user.is_authenticated:
            return redirect('core:dashboard')
        
        context = {
            'keycloak_config': {
                'server_url': settings.KEYCLOAK_CONFIG['SERVER_URL'],
                'realm': settings.KEYCLOAK_CONFIG['REALM'],
                'client_id': settings.KEYCLOAK_CONFIG['CLIENT_ID'],
            },
            'title': 'Royal Kingdom Login',
            'subtitle': 'Enter the Glorious Space Realm'
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request):
        """
        Handle login form submission
        """
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return self.get(request)
        
        # Authenticate with Keycloak
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            messages.success(request, f'Welcome to the royal kingdom, {user.display_name}!')
            
            # Redirect to next page or dashboard
            next_url = request.GET.get('next', reverse('core:dashboard'))
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid credentials. Please check your username and password.')
            return self.get(request)


@method_decorator(csrf_exempt, name='dispatch')
class KeycloakTokenLoginView(View):
    """
    Handle Keycloak token-based authentication
    """
    
    def post(self, request):
        """
        Authenticate using Keycloak access token
        """
        try:
            data = json.loads(request.body)
            access_token = data.get('access_token')
            
            if not access_token:
                return JsonResponse({
                    'success': False,
                    'error': 'Access token is required'
                }, status=400)
            
            # Authenticate with token
            user = authenticate(request, access_token=access_token)
            
            if user:
                login(request, user)
                return JsonResponse({
                    'success': True,
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'display_name': user.display_name,
                    },
                    'redirect_url': reverse('core:dashboard')
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid token'
                }, status=401)
                
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            logger.error(f"Token login error: {e}")
            return JsonResponse({
                'success': False,
                'error': 'Authentication failed'
            }, status=500)


@login_required
def keycloak_logout_view(request):
    """
    Handle Keycloak logout
    """
    # Get refresh token from session
    keycloak_token = request.session.get('keycloak_token')
    
    if keycloak_token and 'refresh_token' in keycloak_token:
        # Logout from Keycloak
        logout_success = logout_keycloak_user(keycloak_token['refresh_token'])
        if logout_success:
            logger.info(f"Successfully logged out user {request.user.username} from Keycloak")
        else:
            logger.warning(f"Failed to logout user {request.user.username} from Keycloak")
    
    # Clear Django session
    logout(request)
    messages.info(request, 'You have been successfully logged out.')
    
    return redirect('core:home')


@csrf_exempt
@require_http_methods(["POST"])
def refresh_token_view(request):
    """
    Refresh Keycloak access token
    """
    try:
        data = json.loads(request.body)
        refresh_token = data.get('refresh_token')
        
        if not refresh_token:
            return JsonResponse({
                'success': False,
                'error': 'Refresh token is required'
            }, status=400)
        
        # Refresh token
        new_token = refresh_keycloak_token(refresh_token)
        
        if new_token:
            # Update session with new token
            request.session['keycloak_token'] = new_token
            
            return JsonResponse({
                'success': True,
                'access_token': new_token['access_token'],
                'refresh_token': new_token['refresh_token'],
                'expires_in': new_token['expires_in']
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Token refresh failed'
            }, status=401)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        return JsonResponse({
            'success': False,
            'error': 'Token refresh failed'
        }, status=500)


class KeycloakRegisterView(View):
    """
    Handle user registration with Keycloak
    """
    template_name = 'auth/keycloak_register.html'
    
    def get(self, request):
        """
        Display registration form
        """
        if request.user.is_authenticated:
            return redirect('core:dashboard')
        
        context = {
            'title': 'Join the Royal Kingdom',
            'subtitle': 'Create your account in Glorious Space'
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request):
        """
        Handle registration form submission
        """
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        
        if not all([username, email, password]):
            messages.error(request, 'Username, email, and password are required.')
            return self.get(request)
        
        try:
            # Create user in Keycloak
            user_data = {
                'username': username,
                'email': email,
                'firstName': first_name,
                'lastName': last_name,
                'enabled': True,
                'credentials': [{
                    'type': 'password',
                    'value': password,
                    'temporary': False
                }]
            }
            
            keycloak_user_id = create_keycloak_user(user_data)
            
            if keycloak_user_id:
                messages.success(request, 
                    'Account created successfully! You can now log in with your credentials.')
                return redirect('auth:keycloak_login')
            else:
                messages.error(request, 
                    'Failed to create account. Please try again or contact support.')
                return self.get(request)
                
        except Exception as e:
            logger.error(f"Registration error: {e}")
            messages.error(request, 
                'An error occurred during registration. Please try again.')
            return self.get(request)


@login_required
def user_profile_view(request):
    """
    Display user profile with Keycloak integration
    """
    context = {
        'title': 'Royal Profile',
        'user': request.user,
        'keycloak_token': request.session.get('keycloak_token'),
    }
    
    return render(request, 'auth/profile.html', context)


@csrf_exempt
@require_http_methods(["GET"])
def keycloak_status_view(request):
    """
    Check Keycloak server status
    """
    try:
        admin = get_keycloak_admin()
        server_info = admin.get_server_info()
        
        return JsonResponse({
            'success': True,
            'status': 'online',
            'server_info': {
                'product_name': server_info.get('productName', 'Unknown'),
                'product_version': server_info.get('productVersion', 'Unknown'),
            }
        })
    except Exception as e:
        logger.error(f"Keycloak status check failed: {e}")
        return JsonResponse({
            'success': False,
            'status': 'offline',
            'error': str(e)
        }, status=503)


def keycloak_callback_view(request):
    """
    Handle Keycloak OAuth callback
    """
    # This view handles the OAuth callback from Keycloak
    # Usually handled by django-allauth, but we can customize it here
    
    authorization_code = request.GET.get('code')
    state = request.GET.get('state')
    
    if not authorization_code:
        messages.error(request, 'Authorization failed. Please try again.')
        return redirect('auth:keycloak_login')
    
    # Here you would exchange the authorization code for tokens
    # This is typically handled by the OAuth provider (allauth)
    
    messages.success(request, 'Successfully authenticated with Keycloak!')
    return redirect('core:dashboard')
