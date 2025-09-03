# WebSocket Consumers for Glorious Space - Real-time Magic
# Where Instant Communication Comes Alive

import json
import asyncio
from datetime import datetime
from typing import Dict, List, Any

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    """
    Real-time Chat Consumer for Live Communication
    Handles multiple chat rooms with voice/video capabilities
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_name = None
        self.room_group_name = None
        self.user = None
        self.user_count = 0
        
    async def connect(self):
        """Establish WebSocket connection and join chat room"""
        try:
            # Extract room name from URL
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = f'chat_{self.room_name}'
            
            # Get user from scope
            self.user = self.scope.get('user', AnonymousUser())
            
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            
            # Accept WebSocket connection
            await self.accept()
            
            # Update user count and notify others
            await self.update_user_count(1)
            await self.send_user_joined_notification()
            
        except Exception as e:
            await self.close(code=4000)
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        if self.room_group_name:
            # Update user count and notify others
            await self.update_user_count(-1)
            await self.send_user_left_notification()
            
            # Leave room group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
    
    async def receive(self, text_data):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(text_data)
            message_type = data.get('type', 'chat_message')
            
            # Route message based on type
            if message_type == 'chat_message':
                await self.handle_chat_message(data)
            elif message_type == 'typing_indicator':
                await self.handle_typing_indicator(data)
            elif message_type == 'voice_signal':
                await self.handle_voice_signal(data)
            elif message_type == 'video_signal':
                await self.handle_video_signal(data)
            elif message_type == 'message_reaction':
                await self.handle_message_reaction(data)
            elif message_type == 'file_share':
                await self.handle_file_share(data)
            else:
                await self.send_error('Unknown message type')
                
        except json.JSONDecodeError:
            await self.send_error('Invalid JSON format')
        except Exception as e:
            await self.send_error(f'Message processing error: {str(e)}')
    
    async def handle_chat_message(self, data):
        """Process and broadcast chat messages"""
        message = data.get('message', '').strip()
        
        if not message:
            return
            
        # Create message object
        message_data = {
            'type': 'chat_message',
            'message': message,
            'username': self.user.username if self.user.is_authenticated else 'Anonymous',
            'user_id': self.user.id if self.user.is_authenticated else None,
            'timestamp': datetime.now().isoformat(),
            'room': self.room_name,
            'message_id': await self.generate_message_id(),
        }
        
        # Save message to database
        if self.user.is_authenticated:
            await self.save_chat_message(message_data)
        
        # Broadcast to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message_broadcast',
                'message_data': message_data
            }
        )
    
    async def handle_typing_indicator(self, data):
        """Handle typing indicator signals"""
        if not self.user.is_authenticated:
            return
            
        typing_data = {
            'type': 'typing_indicator',
            'username': self.user.username,
            'user_id': self.user.id,
            'is_typing': data.get('is_typing', False),
            'timestamp': datetime.now().isoformat(),
        }
        
        # Broadcast typing indicator to others (not self)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'typing_indicator_broadcast',
                'typing_data': typing_data,
                'sender_channel': self.channel_name
            }
        )
    
    async def handle_voice_signal(self, data):
        """Handle WebRTC voice signaling"""
        signal_data = {
            'type': 'voice_signal',
            'signal_type': data.get('signal_type'),  # offer, answer, ice-candidate
            'signal_data': data.get('signal_data'),
            'from_user': self.user.username if self.user.is_authenticated else 'Anonymous',
            'from_user_id': self.user.id if self.user.is_authenticated else None,
            'to_user_id': data.get('to_user_id'),
            'timestamp': datetime.now().isoformat(),
        }
        
        # Send to specific user or broadcast to room
        if signal_data['to_user_id']:
            await self.send_to_user(signal_data['to_user_id'], signal_data)
        else:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'voice_signal_broadcast',
                    'signal_data': signal_data
                }
            )
    
    async def handle_video_signal(self, data):
        """Handle WebRTC video signaling"""
        signal_data = {
            'type': 'video_signal',
            'signal_type': data.get('signal_type'),
            'signal_data': data.get('signal_data'),
            'from_user': self.user.username if self.user.is_authenticated else 'Anonymous',
            'from_user_id': self.user.id if self.user.is_authenticated else None,
            'to_user_id': data.get('to_user_id'),
            'timestamp': datetime.now().isoformat(),
        }
        
        # Send to specific user or broadcast to room
        if signal_data['to_user_id']:
            await self.send_to_user(signal_data['to_user_id'], signal_data)
        else:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'video_signal_broadcast',
                    'signal_data': signal_data
                }
            )
    
    async def handle_message_reaction(self, data):
        """Handle message reactions (like, love, laugh, etc.)"""
        reaction_data = {
            'type': 'message_reaction',
            'message_id': data.get('message_id'),
            'reaction': data.get('reaction'),  # emoji or reaction type
            'username': self.user.username if self.user.is_authenticated else 'Anonymous',
            'user_id': self.user.id if self.user.is_authenticated else None,
            'timestamp': datetime.now().isoformat(),
        }
        
        # Save reaction to database
        if self.user.is_authenticated:
            await self.save_message_reaction(reaction_data)
        
        # Broadcast reaction to room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'message_reaction_broadcast',
                'reaction_data': reaction_data
            }
        )
    
    async def handle_file_share(self, data):
        """Handle file sharing in chat"""
        file_data = {
            'type': 'file_share',
            'file_name': data.get('file_name'),
            'file_size': data.get('file_size'),
            'file_type': data.get('file_type'),
            'file_url': data.get('file_url'),
            'username': self.user.username if self.user.is_authenticated else 'Anonymous',
            'user_id': self.user.id if self.user.is_authenticated else None,
            'timestamp': datetime.now().isoformat(),
        }
        
        # Save file share to database
        if self.user.is_authenticated:
            await self.save_file_share(file_data)
        
        # Broadcast file share to room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'file_share_broadcast',
                'file_data': file_data
            }
        )
    
    # Broadcast handlers
    async def chat_message_broadcast(self, event):
        """Send chat message to WebSocket"""
        await self.send(text_data=json.dumps(event['message_data']))
    
    async def typing_indicator_broadcast(self, event):
        """Send typing indicator to WebSocket (exclude sender)"""
        if self.channel_name != event['sender_channel']:
            await self.send(text_data=json.dumps(event['typing_data']))
    
    async def voice_signal_broadcast(self, event):
        """Send voice signal to WebSocket"""
        await self.send(text_data=json.dumps(event['signal_data']))
    
    async def video_signal_broadcast(self, event):
        """Send video signal to WebSocket"""
        await self.send(text_data=json.dumps(event['signal_data']))
    
    async def message_reaction_broadcast(self, event):
        """Send message reaction to WebSocket"""
        await self.send(text_data=json.dumps(event['reaction_data']))
    
    async def file_share_broadcast(self, event):
        """Send file share notification to WebSocket"""
        await self.send(text_data=json.dumps(event['file_data']))
    
    async def user_count_update(self, event):
        """Send user count update to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'user_count_update',
            'count': event['count']
        }))
    
    async def user_joined_notification(self, event):
        """Send user joined notification to WebSocket"""
        await self.send(text_data=json.dumps(event['notification_data']))
    
    async def user_left_notification(self, event):
        """Send user left notification to WebSocket"""
        await self.send(text_data=json.dumps(event['notification_data']))
    
    # Helper methods
    async def send_error(self, error_message):
        """Send error message to client"""
        await self.send(text_data=json.dumps({
            'type': 'error',
            'message': error_message,
            'timestamp': datetime.now().isoformat()
        }))
    
    async def update_user_count(self, delta):
        """Update and broadcast user count"""
        # This would typically use Redis or database to track user count
        # For now, we'll simulate it
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_count_update',
                'count': await self.get_room_user_count()
            }
        )
    
    async def send_user_joined_notification(self):
        """Notify room that user joined"""
        if self.user.is_authenticated:
            notification_data = {
                'type': 'user_joined',
                'username': self.user.username,
                'user_id': self.user.id,
                'timestamp': datetime.now().isoformat(),
                'message': f'{self.user.username} joined the chat'
            }
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_joined_notification',
                    'notification_data': notification_data
                }
            )
    
    async def send_user_left_notification(self):
        """Notify room that user left"""
        if self.user.is_authenticated:
            notification_data = {
                'type': 'user_left',
                'username': self.user.username,
                'user_id': self.user.id,
                'timestamp': datetime.now().isoformat(),
                'message': f'{self.user.username} left the chat'
            }
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_left_notification',
                    'notification_data': notification_data
                }
            )
    
    async def send_to_user(self, user_id, data):
        """Send message to specific user"""
        # This would require tracking user channels by user_id
        # For now, we'll broadcast to the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'direct_message',
                'message_data': data,
                'target_user_id': user_id
            }
        )
    
    # Database operations (async wrappers)
    @database_sync_to_async
    def save_chat_message(self, message_data):
        """Save chat message to database"""
        # Implementation would save to ChatMessage model
        pass
    
    @database_sync_to_async
    def save_message_reaction(self, reaction_data):
        """Save message reaction to database"""
        # Implementation would save to MessageReaction model
        pass
    
    @database_sync_to_async
    def save_file_share(self, file_data):
        """Save file share to database"""
        # Implementation would save to FileShare model
        pass
    
    @database_sync_to_async
    def generate_message_id(self):
        """Generate unique message ID"""
        import uuid
        return str(uuid.uuid4())
    
    @database_sync_to_async
    def get_room_user_count(self):
        """Get current user count in room"""
        # This would query actual user count from Redis/DB
        return 1


class CollaborationConsumer(AsyncWebsocketConsumer):
    """
    Real-time Collaboration Consumer for Code Editing
    Handles collaborative coding sessions with live cursor tracking
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session_id = None
        self.session_group_name = None
        self.user = None
    
    async def connect(self):
        """Establish WebSocket connection for collaboration session"""
        try:
            self.session_id = self.scope['url_route']['kwargs']['session_id']
            self.session_group_name = f'collaboration_{self.session_id}'
            self.user = self.scope.get('user', AnonymousUser())
            
            # Join collaboration session
            await self.channel_layer.group_add(
                self.session_group_name,
                self.channel_name
            )
            
            await self.accept()
            
            # Notify others of new collaborator
            await self.send_collaborator_joined()
            
        except Exception as e:
            await self.close(code=4000)
    
    async def disconnect(self, close_code):
        """Handle collaboration session disconnect"""
        if self.session_group_name:
            await self.send_collaborator_left()
            
            await self.channel_layer.group_discard(
                self.session_group_name,
                self.channel_name
            )
    
    async def receive(self, text_data):
        """Handle collaboration events"""
        try:
            data = json.loads(text_data)
            event_type = data.get('type')
            
            if event_type == 'code_change':
                await self.handle_code_change(data)
            elif event_type == 'cursor_position':
                await self.handle_cursor_position(data)
            elif event_type == 'selection_change':
                await self.handle_selection_change(data)
            elif event_type == 'file_change':
                await self.handle_file_change(data)
            elif event_type == 'voice_chat':
                await self.handle_voice_chat(data)
            
        except json.JSONDecodeError:
            await self.send_error('Invalid JSON format')
        except Exception as e:
            await self.send_error(f'Collaboration error: {str(e)}')
    
    async def handle_code_change(self, data):
        """Handle real-time code changes"""
        change_data = {
            'type': 'code_change',
            'file_path': data.get('file_path'),
            'changes': data.get('changes'),  # Array of change operations
            'user_id': self.user.id if self.user.is_authenticated else None,
            'username': self.user.username if self.user.is_authenticated else 'Anonymous',
            'timestamp': datetime.now().isoformat(),
        }
        
        # Broadcast to all collaborators except sender
        await self.channel_layer.group_send(
            self.session_group_name,
            {
                'type': 'code_change_broadcast',
                'change_data': change_data,
                'sender_channel': self.channel_name
            }
        )
    
    async def handle_cursor_position(self, data):
        """Handle cursor position updates"""
        cursor_data = {
            'type': 'cursor_position',
            'file_path': data.get('file_path'),
            'line': data.get('line'),
            'column': data.get('column'),
            'user_id': self.user.id if self.user.is_authenticated else None,
            'username': self.user.username if self.user.is_authenticated else 'Anonymous',
            'user_color': data.get('user_color', '#667eea'),
        }
        
        # Broadcast cursor position to others
        await self.channel_layer.group_send(
            self.session_group_name,
            {
                'type': 'cursor_position_broadcast',
                'cursor_data': cursor_data,
                'sender_channel': self.channel_name
            }
        )
    
    async def send_collaborator_joined(self):
        """Notify session of new collaborator"""
        if self.user.is_authenticated:
            join_data = {
                'type': 'collaborator_joined',
                'user_id': self.user.id,
                'username': self.user.username,
                'timestamp': datetime.now().isoformat(),
            }
            
            await self.channel_layer.group_send(
                self.session_group_name,
                {
                    'type': 'collaborator_joined_broadcast',
                    'join_data': join_data,
                    'sender_channel': self.channel_name
                }
            )
    
    # Broadcast handlers
    async def code_change_broadcast(self, event):
        """Broadcast code changes to other collaborators"""
        if self.channel_name != event['sender_channel']:
            await self.send(text_data=json.dumps(event['change_data']))
    
    async def cursor_position_broadcast(self, event):
        """Broadcast cursor position to other collaborators"""
        if self.channel_name != event['sender_channel']:
            await self.send(text_data=json.dumps(event['cursor_data']))
    
    async def collaborator_joined_broadcast(self, event):
        """Broadcast new collaborator notification"""
        if self.channel_name != event['sender_channel']:
            await self.send(text_data=json.dumps(event['join_data']))


class NotificationConsumer(AsyncWebsocketConsumer):
    """
    Real-time Notification Consumer
    Handles live notifications for users across the platform
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.user_group_name = None
    
    async def connect(self):
        """Connect to user's notification channel"""
        self.user = self.scope.get('user', AnonymousUser())
        
        if not self.user.is_authenticated:
            await self.close(code=4001)
            return
        
        self.user_group_name = f'notifications_{self.user.id}'
        
        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send unread notification count
        await self.send_unread_count()
    
    async def disconnect(self, close_code):
        """Disconnect from notification channel"""
        if self.user_group_name:
            await self.channel_layer.group_discard(
                self.user_group_name,
                self.channel_name
            )
    
    async def receive(self, text_data):
        """Handle notification actions"""
        try:
            data = json.loads(text_data)
            action = data.get('action')
            
            if action == 'mark_read':
                await self.mark_notification_read(data.get('notification_id'))
            elif action == 'mark_all_read':
                await self.mark_all_notifications_read()
            
        except json.JSONDecodeError:
            pass
    
    async def notification_broadcast(self, event):
        """Send notification to user"""
        await self.send(text_data=json.dumps(event['notification_data']))
    
    async def send_unread_count(self):
        """Send current unread notification count"""
        count = await self.get_unread_count()
        await self.send(text_data=json.dumps({
            'type': 'unread_count',
            'count': count
        }))
    
    @database_sync_to_async
    def get_unread_count(self):
        """Get unread notification count for user"""
        # Implementation would query Notification model
        return 0
    
    @database_sync_to_async
    def mark_notification_read(self, notification_id):
        """Mark specific notification as read"""
        # Implementation would update Notification model
        pass
    
    @database_sync_to_async
    def mark_all_notifications_read(self):
        """Mark all notifications as read for user"""
        # Implementation would update all user notifications
        pass
