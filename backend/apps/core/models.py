from django.db import models
from django.conf import settings


class Project(models.Model):
    """Developer projects with canvas integration"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    technologies = models.JSONField(default=list)
    github_url = models.URLField(blank=True, null=True)
    demo_url = models.URLField(blank=True, null=True)
    canvas_data = models.JSONField(default=dict, blank=True)  # Store canvas visualizations
    is_public = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    likes_count = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class CanvasSession(models.Model):
    """Canvas sessions for 2D/3D/4D rendering"""
    CANVAS_TYPES = [
        ('2d', '2D Canvas'),
        ('3d', '3D WebGL'),
        ('4d', '4D Simulation'),
        ('5g', '5G Real-time'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='canvas_sessions')
    session_name = models.CharField(max_length=200)
    canvas_type = models.CharField(max_length=10, choices=CANVAS_TYPES, default='2d')
    canvas_data = models.JSONField(default=dict)  # Store canvas state and objects
    is_public = models.BooleanField(default=False)
    is_collaborative = models.BooleanField(default=False)
    collaborators = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='collaborative_sessions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.session_name} ({self.canvas_type})"


class CodeSnippet(models.Model):
    """Code snippets shared by developers"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    code = models.TextField()
    language = models.CharField(max_length=50)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='code_snippets')
    tags = models.JSONField(default=list)
    is_public = models.BooleanField(default=True)
    likes_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class TechStack(models.Model):
    """Technology stacks for projects"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=50)  # frontend, backend, database, etc.
    icon_url = models.URLField(blank=True, null=True)
    official_website = models.URLField(blank=True, null=True)
    popularity_score = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.name


class Collaboration(models.Model):
    """Real-time collaboration sessions"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hosted_collaborations')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='joined_collaborations')
    session_type = models.CharField(max_length=20, choices=[
        ('canvas', 'Canvas Collaboration'),
        ('code', 'Code Review'),
        ('brainstorm', 'Brainstorming'),
        ('5g_demo', '5G Demo Session')
    ])
    is_active = models.BooleanField(default=True)
    room_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
