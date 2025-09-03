# WebSocket Routing for Glorious Space - The Real-time Pathways
# Where Instant Communication Flows Like Digital Rivers

from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    # Chat WebSocket Routes - The Communication Channels
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/chat/room/(?P<room_name>[\w-]+)/$', consumers.ChatConsumer.as_asgi()),
    
    # Collaboration WebSocket Routes - The Workshop Connections
    re_path(r'ws/collaboration/(?P<session_id>[\w-]+)/$', consumers.CollaborationConsumer.as_asgi()),
    re_path(r'ws/collab/(?P<session_id>[\w-]+)/$', consumers.CollaborationConsumer.as_asgi()),
    
    # Notification WebSocket Routes - The Royal Message System
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
    re_path(r'ws/notify/$', consumers.NotificationConsumer.as_asgi()),
    
    # AI Chat WebSocket Routes - The Oracle Connections
    re_path(r'ws/ai-chat/(?P<conversation_id>[\w-]+)/$', consumers.ChatConsumer.as_asgi()),
    
    # Canvas Collaboration Routes - The Creative Forge
    re_path(r'ws/canvas/(?P<canvas_id>[\w-]+)/$', consumers.CollaborationConsumer.as_asgi()),
    
    # General Real-time Routes
    re_path(r'ws/general/$', consumers.ChatConsumer.as_asgi()),
]
