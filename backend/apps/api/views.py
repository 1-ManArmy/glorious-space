from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from backend.apps.users.models import CustomUser, DeveloperProfile
from backend.apps.core.models import Project, CanvasSession
from .serializers import (
    UserSerializer, DeveloperProfileSerializer, 
    ProjectSerializer, CanvasSessionSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.action == 'list':
            # Only return public developer profiles
            return CustomUser.objects.filter(is_developer=True, is_active=True)
        return super().get_queryset()
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class DeveloperProfileViewSet(viewsets.ModelViewSet):
    queryset = DeveloperProfile.objects.all()
    serializer_class = DeveloperProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return DeveloperProfile.objects.all()
        return DeveloperProfile.objects.none()


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Project.objects.filter(is_public=True)
        if self.request.user.is_authenticated:
            # Include user's private projects
            user_projects = Project.objects.filter(owner=self.request.user)
            queryset = queryset.union(user_projects)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_projects(self, request):
        """Get current user's projects"""
        projects = Project.objects.filter(owner=request.user)
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)


class CanvasSessionViewSet(viewsets.ModelViewSet):
    queryset = CanvasSession.objects.all()
    serializer_class = CanvasSessionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return CanvasSession.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def share_session(self, request, pk=None):
        """Share canvas session in real-time"""
        session = self.get_object()
        channel_layer = get_channel_layer()
        
        # Broadcast to all users in the canvas room
        async_to_sync(channel_layer.group_send)(
            f"canvas_{session.id}",
            {
                "type": "canvas_update",
                "session_id": session.id,
                "canvas_data": session.canvas_data,
                "user": request.user.username
            }
        )
        
        return Response({"status": "Canvas session shared successfully"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_data(request):
    """Get dashboard data for authenticated user"""
    user = request.user
    profile = user.developer_profile
    
    # Get user's projects
    projects = Project.objects.filter(owner=user)[:5]
    
    # Get recent canvas sessions
    canvas_sessions = CanvasSession.objects.filter(user=user)[:5]
    
    # Get community stats
    total_developers = CustomUser.objects.filter(is_developer=True, is_active=True).count()
    total_projects = Project.objects.filter(is_public=True).count()
    
    data = {
        'user': UserSerializer(user).data,
        'profile': DeveloperProfileSerializer(profile).data,
        'recent_projects': ProjectSerializer(projects, many=True).data,
        'recent_canvas_sessions': CanvasSessionSerializer(canvas_sessions, many=True).data,
        'community_stats': {
            'total_developers': total_developers,
            'total_projects': total_projects,
            'total_canvas_sessions': CanvasSession.objects.filter(is_public=True).count()
        }
    }
    
    return Response(data)


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_canvas_data(request):
    """Save canvas data for real-time collaboration"""
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        canvas_data = data.get('canvas_data')
        canvas_type = data.get('canvas_type', '2d')
        
        if session_id:
            # Update existing session
            session = CanvasSession.objects.get(id=session_id, user=request.user)
            session.canvas_data = canvas_data
            session.save()
        else:
            # Create new session
            session = CanvasSession.objects.create(
                user=request.user,
                session_name=f"Canvas Session {CanvasSession.objects.filter(user=request.user).count() + 1}",
                canvas_type=canvas_type,
                canvas_data=canvas_data
            )
        
        # Broadcast to WebSocket if in collaboration mode
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"canvas_{session.id}",
            {
                "type": "canvas_update",
                "session_id": session.id,
                "canvas_data": canvas_data,
                "user": request.user.username
            }
        )
        
        return JsonResponse({
            'status': 'success',
            'session_id': session.id,
            'message': 'Canvas data saved successfully'
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
