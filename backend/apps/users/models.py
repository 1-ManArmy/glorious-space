from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Custom user model with Keycloak integration fields"""
    keycloak_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    profile_picture = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    github_username = models.CharField(max_length=100, blank=True, null=True)
    linkedin_profile = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    skills = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_developer = models.BooleanField(default=True)
    preferred_language = models.CharField(max_length=50, default='Python')
    
    def __str__(self):
        return self.username


class DeveloperProfile(models.Model):
    """Extended profile for developers"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='developer_profile')
    experience_level = models.CharField(
        max_length=20,
        choices=[
            ('junior', 'Junior'),
            ('mid', 'Mid-level'),
            ('senior', 'Senior'),
            ('lead', 'Lead'),
            ('architect', 'Architect')
        ],
        default='junior'
    )
    specializations = models.JSONField(default=list, blank=True)
    portfolio_projects = models.JSONField(default=list, blank=True)
    canvas_preferences = models.JSONField(default=dict, blank=True)  # For 2D/3D/4D preferences
    
    def __str__(self):
        return f"{self.user.username}'s Developer Profile"
