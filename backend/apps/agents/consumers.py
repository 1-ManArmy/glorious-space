"""
Advanced Real-time Communication with WebSockets
Professional WebSocket consumers for agent chat system
"""

import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.utils import timezone
from .models import AgentProfile, UserAgentInteraction, ConversationMemory
from .ai_engine import ConversationEngine, MemoryManager
import logging

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    """Advanced WebSocket consumer for real-time agent chat"""
    
    async def connect(self):
        """Handle WebSocket connection"""
        self.agent_type = self.scope['url_route']['kwargs']['agent_type']
        self.user_id = self.scope.get('user_id', 1)  # Default or from session
        self.room_group_name = f'chat_{self.agent_type}_{self.user_id}'
        
        # Verify agent exists and is active
        try:
            self.agent = await self.get_agent(self.agent_type)
            if not self.agent or not self.agent.is_active:
                await self.close(code=4004)  # Agent not found or inactive
                return
        except Exception as e:
            logger.error(f"Error connecting to agent {self.agent_type}: {str(e)}")
            await self.close(code=4000)  # General error
            return
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send welcome message
        await self.send_agent_message({
            'type': 'system',
            'message': f"Connected to {self.agent.name}! How can I help you today?",
            'agent_info': {
                'name': self.agent.name,
                'type': self.agent_type,
                'capabilities': self.agent.capabilities[:5],  # First 5 capabilities
                'personality': self.get_personality_summary()
            }
        })
        
        logger.info(f"User {self.user_id} connected to {self.agent.name}")
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        # Leave room group
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        
        logger.info(f"User {self.user_id} disconnected from {self.agent_type} (code: {close_code})")
    
    async def receive(self, text_data):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(text_data)
            message_type = data.get('type', 'chat')
            
            if message_type == 'chat':
                await self.handle_chat_message(data)
            elif message_type == 'typing':
                await self.handle_typing_indicator(data)
            elif message_type == 'feedback':
                await self.handle_feedback(data)
            elif message_type == 'get_suggestions':
                await self.handle_get_suggestions(data)
            else:
                await self.send_error("Unknown message type")
                
        except json.JSONDecodeError:
            await self.send_error("Invalid JSON format")
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            await self.send_error("Message processing failed")
    
    async def handle_chat_message(self, data):
        """Process chat message with advanced AI"""
        message = data.get('message', '').strip()
        context = data.get('context', {})
        
        if not message:
            await self.send_error("Message cannot be empty")
            return
        
        # Show typing indicator
        await self.send_typing_indicator(True)
        
        try:
            # Initialize conversation engine
            engine = ConversationEngine(self.agent_type, self.user_id)
            
            # Process message with AI
            response_data = await engine.process_message(message, context)
            
            # Store interaction in database
            interaction = await self.store_interaction(
                message, response_data, context
            )
            
            # Send response to user
            await self.send_agent_message({
                'type': 'response',
                'message': response_data['response'],
                'emotional_state': response_data.get('emotional_state'),
                'confidence': response_data.get('confidence'),
                'conversation_id': response_data.get('conversation_id'),
                'interaction_id': interaction.id if interaction else None,
                'timestamp': timezone.now().isoformat(),
                'suggestions': await self.get_conversation_suggestions(message, response_data)
            })
            
            # Update agent's last interaction time
            await self.update_agent_last_interaction()
            
        except Exception as e:
            logger.error(f"Error processing chat message: {str(e)}")
            await self.send_error("Sorry, I encountered an issue processing your message. Please try again.")
        finally:
            # Hide typing indicator
            await self.send_typing_indicator(False)
    
    async def handle_typing_indicator(self, data):
        """Handle typing indicator from user"""
        is_typing = data.get('is_typing', False)
        
        # Broadcast typing status to room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'typing_status',
                'user_id': self.user_id,
                'is_typing': is_typing
            }
        )
    
    async def handle_feedback(self, data):
        """Handle user feedback on agent responses"""
        interaction_id = data.get('interaction_id')
        rating = data.get('rating')  # 1-5 scale
        feedback_text = data.get('feedback', '')
        
        try:
            success = await self.store_feedback(interaction_id, rating, feedback_text)
            
            if success:
                await self.send_system_message("Thank you for your feedback! It helps me improve.")
                
                # If rating is low, offer assistance
                if rating and rating <= 2:
                    await self.send_system_message(
                        "I notice you weren't satisfied with my response. "
                        "Could you help me understand how I can do better?"
                    )
            else:
                await self.send_error("Failed to record feedback")
                
        except Exception as e:
            logger.error(f"Error handling feedback: {str(e)}")
            await self.send_error("Failed to process feedback")
    
    async def handle_get_suggestions(self, data):
        """Get conversation suggestions for user"""
        try:
            suggestions = await self.get_agent_suggestions()
            
            await self.send_agent_message({
                'type': 'suggestions',
                'suggestions': suggestions
            })
            
        except Exception as e:
            logger.error(f"Error getting suggestions: {str(e)}")
            await self.send_error("Failed to get suggestions")
    
    async def send_agent_message(self, message_data):
        """Send message from agent to user"""
        await self.send(text_data=json.dumps({
            'source': 'agent',
            'agent_name': self.agent.name,
            'agent_type': self.agent_type,
            **message_data
        }))
    
    async def send_system_message(self, message):
        """Send system message"""
        await self.send(text_data=json.dumps({
            'source': 'system',
            'type': 'system',
            'message': message,
            'timestamp': timezone.now().isoformat()
        }))
    
    async def send_error(self, error_message):
        """Send error message"""
        await self.send(text_data=json.dumps({
            'source': 'system',
            'type': 'error',
            'message': error_message,
            'timestamp': timezone.now().isoformat()
        }))
    
    async def send_typing_indicator(self, is_typing):
        """Send typing indicator"""
        await self.send(text_data=json.dumps({
            'source': 'agent',
            'type': 'typing',
            'is_typing': is_typing,
            'agent_name': self.agent.name
        }))
    
    async def typing_status(self, event):
        """Handle typing status broadcast"""
        await self.send(text_data=json.dumps({
            'source': 'user',
            'type': 'typing_status',
            'user_id': event['user_id'],
            'is_typing': event['is_typing']
        }))
    
    def get_personality_summary(self):
        """Get agent personality summary for connection"""
        if not self.agent.personality_traits:
            return "Friendly and helpful"
        
        # Get top 3 personality traits
        sorted_traits = sorted(
            self.agent.personality_traits.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]
        
        trait_descriptions = {
            'empathy': 'empathetic',
            'creativity': 'creative',
            'analytical': 'analytical',
            'humor': 'humorous',
            'professional': 'professional',
            'romantic': 'romantic',
            'technical': 'technical',
            'supportive': 'supportive'
        }
        
        personality_words = [
            trait_descriptions.get(trait, trait.replace('_', ' '))
            for trait, _ in sorted_traits
        ]
        
        return ', '.join(personality_words)
    
    async def get_conversation_suggestions(self, user_message, response_data):
        """Get contextual conversation suggestions"""
        suggestions = []
        
        # Agent-specific suggestions
        if self.agent_type == 'ai_girlfriend_luvie':
            suggestions = [
                "Tell me about your day",
                "I need some emotional support",
                "Share something romantic with me",
                "What do you love about me?"
            ]
        elif self.agent_type == 'claude_king':
            suggestions = [
                "Help me debug this code",
                "Explain this programming concept",
                "Review my code architecture",
                "What's the best practice for..."
            ]
        elif self.agent_type == 'business_advisor_pro':
            suggestions = [
                "Analyze this market opportunity",
                "Help me create a business plan",
                "What's my competitive advantage?",
                "Advise on growth strategies"
            ]
        elif self.agent_type == 'fitness_coach':
            suggestions = [
                "Create a workout plan",
                "Help with nutrition advice",
                "Motivate me to exercise",
                "Track my fitness goals"
            ]
        else:
            suggestions = [
                "What can you help me with?",
                "Tell me about your capabilities",
                "How can we work together?",
                "What makes you unique?"
            ]
        
        return suggestions[:4]  # Return max 4 suggestions
    
    async def get_agent_suggestions(self):
        """Get agent-specific conversation starters"""
        return await self.get_conversation_suggestions("", {})
    
    # Database operations
    @database_sync_to_async
    def get_agent(self, agent_type):
        """Get agent from database"""
        try:
            return AgentProfile.objects.get(agent_type=agent_type)
        except AgentProfile.DoesNotExist:
            return None
    
    @database_sync_to_async
    def store_interaction(self, message, response_data, context):
        """Store interaction in database"""
        try:
            interaction = UserAgentInteraction.objects.create(
                agent=self.agent,
                user_id=self.user_id,
                interaction_type='websocket_chat',
                conversation_data={
                    'user_message': message,
                    'agent_response': response_data['response'],
                    'context': context,
                    'emotional_state': response_data.get('emotional_state'),
                    'confidence': response_data.get('confidence'),
                    'timestamp': timezone.now().isoformat()
                }
            )
            return interaction
        except Exception as e:
            logger.error(f"Error storing interaction: {str(e)}")
            return None
    
    @database_sync_to_async
    def store_feedback(self, interaction_id, rating, feedback_text):
        """Store user feedback"""
        try:
            if interaction_id:
                interaction = UserAgentInteraction.objects.get(id=interaction_id)
                interaction.feedback_rating = rating
                interaction.feedback_text = feedback_text
                interaction.save()
                return True
            return False
        except Exception as e:
            logger.error(f"Error storing feedback: {str(e)}")
            return False
    
    @database_sync_to_async
    def update_agent_last_interaction(self):
        """Update agent's last interaction timestamp"""
        try:
            self.agent.last_interaction = timezone.now()
            self.agent.save(update_fields=['last_interaction'])
        except Exception as e:
            logger.error(f"Error updating agent last interaction: {str(e)}")


class AgentStatusConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for agent status updates"""
    
    async def connect(self):
        """Handle connection for status updates"""
        self.room_group_name = 'agent_status'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send current agent status
        await self.send_agent_status_update()
    
    async def disconnect(self, close_code):
        """Handle disconnection"""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def send_agent_status_update(self):
        """Send current agent status"""
        try:
            status_data = await self.get_agent_status_data()
            await self.send(text_data=json.dumps({
                'type': 'status_update',
                'data': status_data,
                'timestamp': timezone.now().isoformat()
            }))
        except Exception as e:
            logger.error(f"Error sending status update: {str(e)}")
    
    async def agent_status_update(self, event):
        """Handle agent status update broadcast"""
        await self.send(text_data=json.dumps({
            'type': 'status_update',
            'data': event['data'],
            'timestamp': event['timestamp']
        }))
    
    @database_sync_to_async
    def get_agent_status_data(self):
        """Get current agent status data"""
        try:
            agents = AgentProfile.objects.filter(is_active=True)
            total_active = agents.count()
            
            # Get recent activity
            recent_interactions = UserAgentInteraction.objects.filter(
                created_at__gte=timezone.now() - timezone.timedelta(hours=1)
            ).count()
            
            return {
                'total_active_agents': total_active,
                'recent_interactions_1h': recent_interactions,
                'system_status': 'operational',
                'last_updated': timezone.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting agent status: {str(e)}")
            return {'error': 'Failed to get status'}


# WebSocket URL routing would be added to routing.py:
"""
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<agent_type>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/agent-status/$', consumers.AgentStatusConsumer.as_asgi()),
]
"""
