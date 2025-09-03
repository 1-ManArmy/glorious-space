import requests
import urllib.parse
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import login
from .keycloak_settings import *
import logging

logger = logging.getLogger(__name__)


class KeycloakAuth:
    """Keycloak authentication handler"""
    
    def __init__(self):
        self.config = KEYCLOAK_CONFIG
        
    def get_login_url(self):
        """Generate Keycloak login URL"""
        params = {
            'client_id': self.config['client_id'],
            'redirect_uri': self.config['redirect_uri'],
            'scope': self.config['scope'],
            'response_type': 'code',
            'state': 'dev-crown-state'  # You should generate a random state
        }
        
        query_string = urllib.parse.urlencode(params)
        return f"{KEYCLOAK_AUTH_URL}?{query_string}"
    
    def exchange_code_for_token(self, authorization_code):
        """Exchange authorization code for access token"""
        try:
            data = {
                'grant_type': 'authorization_code',
                'client_id': self.config['client_id'],
                'client_secret': self.config['client_secret'],
                'redirect_uri': self.config['redirect_uri'],
                'code': authorization_code,
            }
            
            response = requests.post(KEYCLOAK_TOKEN_URL, data=data)
            response.raise_for_status()
            
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"Failed to exchange code for token: {e}")
            return None
    
    def get_user_info(self, access_token):
        """Get user information from Keycloak"""
        try:
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(KEYCLOAK_USERINFO_URL, headers=headers)
            response.raise_for_status()
            
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"Failed to get user info: {e}")
            return None
    
    def handle_callback(self, request):
        """Handle Keycloak callback and return user info"""
        try:
            authorization_code = request.GET.get('code')
            state = request.GET.get('state')
            error = request.GET.get('error')
            
            if error:
                logger.error(f"Keycloak authentication error: {error}")
                return None
            
            if not authorization_code:
                logger.error("No authorization code received")
                return None
            
            # Exchange code for token
            token_data = self.exchange_code_for_token(authorization_code)
            if not token_data:
                return None
            
            access_token = token_data.get('access_token')
            if not access_token:
                logger.error("No access token received")
                return None
            
            # Get user information
            user_info = self.get_user_info(access_token)
            if not user_info:
                return None
            
            # Store tokens in session for later use
            request.session['keycloak_access_token'] = access_token
            request.session['keycloak_refresh_token'] = token_data.get('refresh_token')
            
            return user_info
            
        except Exception as e:
            logger.error(f"Error handling Keycloak callback: {e}")
            return None
    
    def refresh_token(self, refresh_token):
        """Refresh access token using refresh token"""
        try:
            data = {
                'grant_type': 'refresh_token',
                'client_id': self.config['client_id'],
                'client_secret': self.config['client_secret'],
                'refresh_token': refresh_token,
            }
            
            response = requests.post(KEYCLOAK_TOKEN_URL, data=data)
            response.raise_for_status()
            
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"Failed to refresh token: {e}")
            return None
    
    def logout_user(self, refresh_token):
        """Logout user from Keycloak"""
        try:
            data = {
                'client_id': self.config['client_id'],
                'client_secret': self.config['client_secret'],
                'refresh_token': refresh_token,
            }
            
            response = requests.post(KEYCLOAK_LOGOUT_URL, data=data)
            response.raise_for_status()
            
            return True
            
        except requests.RequestException as e:
            logger.error(f"Failed to logout from Keycloak: {e}")
            return False


class KeycloakAdmin:
    """Keycloak admin operations"""
    
    def __init__(self):
        self.admin_config = KEYCLOAK_ADMIN_CONFIG
        self.access_token = None
        
    def get_admin_token(self):
        """Get admin access token"""
        try:
            data = {
                'grant_type': 'password',
                'client_id': 'admin-cli',
                'username': self.admin_config['username'],
                'password': self.admin_config['password'],
            }
            
            response = requests.post(KEYCLOAK_TOKEN_URL, data=data)
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data.get('access_token')
            return self.access_token
            
        except requests.RequestException as e:
            logger.error(f"Failed to get admin token: {e}")
            return None
    
    def create_user(self, user_data):
        """Create user in Keycloak"""
        if not self.access_token:
            self.get_admin_token()
        
        try:
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            create_url = f"{self.admin_config['admin_url']}/users"
            response = requests.post(create_url, json=user_data, headers=headers)
            response.raise_for_status()
            
            return True
            
        except requests.RequestException as e:
            logger.error(f"Failed to create user: {e}")
            return False
    
    def get_users(self):
        """Get all users from Keycloak"""
        if not self.access_token:
            self.get_admin_token()
        
        try:
            headers = {'Authorization': f'Bearer {self.access_token}'}
            users_url = f"{self.admin_config['admin_url']}/users"
            
            response = requests.get(users_url, headers=headers)
            response.raise_for_status()
            
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"Failed to get users: {e}")
            return []
