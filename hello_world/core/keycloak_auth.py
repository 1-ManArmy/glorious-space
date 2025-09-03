# 👑 Keycloak Authentication Backend - Royal Gateway Guardian
# Handles authentication through our Keycloak realm

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.conf import settings
from keycloak import KeycloakOpenID, KeycloakAdmin
from keycloak.exceptions import KeycloakError
import logging
import jwt
from datetime import datetime

logger = logging.getLogger(__name__)
User = get_user_model()


class KeycloakAuthenticationBackend(BaseBackend):
    """
    Custom authentication backend for Keycloak integration
    """
    
    def __init__(self):
        self.keycloak_openid = KeycloakOpenID(
            server_url=settings.KEYCLOAK_CONFIG['SERVER_URL'],
            client_id=settings.KEYCLOAK_CONFIG['CLIENT_ID'],
            realm_name=settings.KEYCLOAK_CONFIG['REALM'],
            client_secret_key=settings.KEYCLOAK_CONFIG['CLIENT_SECRET'],
            verify=settings.KEYCLOAK_CONFIG['VERIFY_SSL']
        )
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate user against Keycloak
        """
        if not username or not password:
            return None
        
        try:
            # Get token from Keycloak
            token = self.keycloak_openid.token(username, password)
            
            if token:
                # Decode user info from token
                user_info = self.keycloak_openid.userinfo(token['access_token'])
                
                # Get or create user
                user = self._get_or_create_user(user_info, token)
                
                # Store token in session for later use
                if hasattr(request, 'session'):
                    request.session['keycloak_token'] = token
                
                logger.info(f"Successfully authenticated user: {username}")
                return user
                
        except KeycloakError as e:
            logger.warning(f"Keycloak authentication failed for {username}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during authentication: {e}")
            return None
    
    def get_user(self, user_id):
        """
        Get user by ID
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
    
    def _get_or_create_user(self, user_info, token):
        """
        Get or create Django user from Keycloak user info
        """
        username = user_info.get('preferred_username')
        email = user_info.get('email', '')
        first_name = user_info.get('given_name', '')
        last_name = user_info.get('family_name', '')
        
        # Try to get existing user
        user = None
        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                pass
        
        if not user:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                pass
        
        # Create new user if doesn't exist
        if not user:
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            logger.info(f"Created new user from Keycloak: {username}")
        else:
            # Update existing user info
            user.email = email or user.email
            user.first_name = first_name or user.first_name
            user.last_name = last_name or user.last_name
            user.save()
            logger.info(f"Updated existing user from Keycloak: {username}")
        
        # Update user profile with Keycloak data
        self._update_user_profile(user, user_info)
        
        return user
    
    def _update_user_profile(self, user, user_info):
        """
        Update user profile with additional Keycloak attributes
        """
        try:
            # Update bio if available
            if hasattr(user, 'bio') and not user.bio:
                bio = user_info.get('bio', '')
                if bio:
                    user.bio = bio
            
            # Update location if available
            if hasattr(user, 'location') and not user.location:
                location = user_info.get('location', '')
                if location:
                    user.location = location
            
            # Update website if available
            if hasattr(user, 'website') and not user.website:
                website = user_info.get('website', '')
                if website:
                    user.website = website
            
            # Set last active
            if hasattr(user, 'last_active'):
                user.last_active = datetime.now()
            
            user.save()
            
        except Exception as e:
            logger.warning(f"Failed to update user profile: {e}")


class KeycloakTokenAuthenticationBackend(BaseBackend):
    """
    Authentication backend for Keycloak JWT tokens
    """
    
    def __init__(self):
        self.keycloak_openid = KeycloakOpenID(
            server_url=settings.KEYCLOAK_CONFIG['SERVER_URL'],
            client_id=settings.KEYCLOAK_CONFIG['CLIENT_ID'],
            realm_name=settings.KEYCLOAK_CONFIG['REALM'],
            client_secret_key=settings.KEYCLOAK_CONFIG['CLIENT_SECRET'],
            verify=settings.KEYCLOAK_CONFIG['VERIFY_SSL']
        )
    
    def authenticate(self, request, access_token=None, **kwargs):
        """
        Authenticate using Keycloak access token
        """
        if not access_token:
            # Try to get token from Authorization header
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header.startswith('Bearer '):
                access_token = auth_header[7:]
            else:
                return None
        
        try:
            # Validate token with Keycloak
            user_info = self.keycloak_openid.userinfo(access_token)
            
            if user_info:
                # Get or create user
                username = user_info.get('preferred_username')
                try:
                    user = User.objects.get(username=username)
                    return user
                except User.DoesNotExist:
                    logger.warning(f"User {username} not found in local database")
                    return None
                    
        except KeycloakError as e:
            logger.warning(f"Token validation failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during token authentication: {e}")
            return None
    
    def get_user(self, user_id):
        """
        Get user by ID
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def get_keycloak_admin():
    """
    Get Keycloak admin client
    """
    return KeycloakAdmin(
        server_url=settings.KEYCLOAK_CONFIG['SERVER_URL'],
        username=settings.KEYCLOAK_CONFIG['ADMIN_USERNAME'],
        password=settings.KEYCLOAK_CONFIG['ADMIN_PASSWORD'],
        realm_name=settings.KEYCLOAK_CONFIG['REALM'],
        client_id=settings.KEYCLOAK_CONFIG['ADMIN_CLIENT_ID'],
        verify=settings.KEYCLOAK_CONFIG['VERIFY_SSL']
    )


def refresh_keycloak_token(refresh_token):
    """
    Refresh Keycloak access token
    """
    keycloak_openid = KeycloakOpenID(
        server_url=settings.KEYCLOAK_CONFIG['SERVER_URL'],
        client_id=settings.KEYCLOAK_CONFIG['CLIENT_ID'],
        realm_name=settings.KEYCLOAK_CONFIG['REALM'],
        client_secret_key=settings.KEYCLOAK_CONFIG['CLIENT_SECRET'],
        verify=settings.KEYCLOAK_CONFIG['VERIFY_SSL']
    )
    
    try:
        return keycloak_openid.refresh_token(refresh_token)
    except KeycloakError as e:
        logger.warning(f"Token refresh failed: {e}")
        return None


def logout_keycloak_user(refresh_token):
    """
    Logout user from Keycloak
    """
    keycloak_openid = KeycloakOpenID(
        server_url=settings.KEYCLOAK_CONFIG['SERVER_URL'],
        client_id=settings.KEYCLOAK_CONFIG['CLIENT_ID'],
        realm_name=settings.KEYCLOAK_CONFIG['REALM'],
        client_secret_key=settings.KEYCLOAK_CONFIG['CLIENT_SECRET'],
        verify=settings.KEYCLOAK_CONFIG['VERIFY_SSL']
    )
    
    try:
        return keycloak_openid.logout(refresh_token)
    except KeycloakError as e:
        logger.warning(f"Logout failed: {e}")
        return False


def create_keycloak_user(user_data):
    """
    Create user in Keycloak
    """
    try:
        admin = get_keycloak_admin()
        user_id = admin.create_user(user_data, exist_ok=False)
        logger.info(f"Created Keycloak user: {user_data.get('username')}")
        return user_id
    except KeycloakError as e:
        logger.error(f"Failed to create Keycloak user: {e}")
        return None


def update_keycloak_user(user_id, user_data):
    """
    Update user in Keycloak
    """
    try:
        admin = get_keycloak_admin()
        admin.update_user(user_id, user_data)
        logger.info(f"Updated Keycloak user: {user_id}")
        return True
    except KeycloakError as e:
        logger.error(f"Failed to update Keycloak user: {e}")
        return False


def get_keycloak_user_groups(user_id):
    """
    Get user groups from Keycloak
    """
    try:
        admin = get_keycloak_admin()
        return admin.get_user_groups(user_id)
    except KeycloakError as e:
        logger.error(f"Failed to get user groups: {e}")
        return []


def assign_keycloak_role(user_id, role_name):
    """
    Assign role to user in Keycloak
    """
    try:
        admin = get_keycloak_admin()
        role = admin.get_realm_role(role_name)
        admin.assign_realm_roles(user_id, [role])
        logger.info(f"Assigned role {role_name} to user {user_id}")
        return True
    except KeycloakError as e:
        logger.error(f"Failed to assign role: {e}")
        return False
