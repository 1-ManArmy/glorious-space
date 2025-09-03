from rest_framework import serializers
from backend.apps.users.models import CustomUser, DeveloperProfile
from backend.apps.core.models import Project, CanvasSession


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'bio', 
                 'github_username', 'linkedin_profile', 'website', 'skills', 
                 'preferred_language', 'is_developer', 'created_at']
        read_only_fields = ['id', 'created_at']


class DeveloperProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = DeveloperProfile
        fields = ['user', 'experience_level', 'specializations', 
                 'portfolio_projects', 'canvas_preferences']


class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'technologies', 
                 'github_url', 'demo_url', 'canvas_data', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CanvasSessionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = CanvasSession
        fields = ['id', 'user', 'session_name', 'canvas_type', 'canvas_data', 
                 'is_public', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
