"""
Django Views for Advanced AI Agent Management
High-level professional API endpoints
"""

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
import asyncio
from datetime import datetime, timedelta

from .models import (
    AgentProfile, UserAgentInteraction, AgentLearningData,
    AgentCapability, ConversationMemory, AgentPerformanceMetrics
)
from .ai_engine import ConversationEngine, MemoryManager, AgentLearningEngine


class AgentDashboardView(View):
    """Main dashboard for agent management"""
    
    def get(self, request):
        """Render agent dashboard with analytics"""
        agents = AgentProfile.objects.all().order_by('name')
        
        # Get performance metrics
        total_conversations = UserAgentInteraction.objects.count()
        avg_satisfaction = AgentPerformanceMetrics.objects.aggregate(
            avg_score=Avg('user_satisfaction_score')
        )['avg_score'] or 0
        
        # Recent activity
        recent_interactions = UserAgentInteraction.objects.select_related(
            'agent', 'user'
        ).order_by('-created_at')[:10]
        
        context = {
            'agents': agents,
            'total_conversations': total_conversations,
            'avg_satisfaction': round(avg_satisfaction, 2),
            'recent_interactions': recent_interactions,
            'dashboard_title': 'DevCrown AI Agent Command Center'
        }
        
        return render(request, 'agents/dashboard.html', context)


class AgentProfileView(View):
    """Individual agent profile and statistics"""
    
    def get(self, request, agent_id):
        """Show detailed agent profile"""
        agent = get_object_or_404(AgentProfile, id=agent_id)
        
        # Get agent statistics
        interactions_count = UserAgentInteraction.objects.filter(agent=agent).count()
        avg_rating = AgentPerformanceMetrics.objects.filter(agent=agent).aggregate(
            avg_rating=Avg('user_satisfaction_score')
        )['avg_rating'] or 0
        
        # Learning progress
        learning_data = AgentLearningData.objects.filter(agent=agent).order_by('-created_at')[:5]
        
        # Capabilities
        capabilities = AgentCapability.objects.filter(agent=agent).order_by('-proficiency_level')
        
        # Recent conversations
        recent_conversations = ConversationMemory.objects.filter(
            agent=agent
        ).order_by('-created_at')[:10]
        
        context = {
            'agent': agent,
            'interactions_count': interactions_count,
            'avg_rating': round(avg_rating, 2),
            'learning_data': learning_data,
            'capabilities': capabilities,
            'recent_conversations': recent_conversations
        }
        
        return render(request, 'agents/profile.html', context)


@method_decorator(csrf_exempt, name='dispatch')
class AgentChatAPI(View):
    """Advanced chat API with all agents"""
    
    def post(self, request):
        """Handle chat messages with advanced AI processing"""
        try:
            data = json.loads(request.body)
            agent_type = data.get('agent_type')
            message = data.get('message')
            user_id = data.get('user_id', 1)  # Default or from session
            context = data.get('context', {})
            
            if not agent_type or not message:
                return JsonResponse({
                    'error': 'Agent type and message are required'
                }, status=400)
            
            # Initialize conversation engine
            engine = ConversationEngine(agent_type, user_id)
            
            # Process message with advanced AI (synchronous for now)
            try:
                response_data = engine.process_message(message, context)
            except Exception as e:
                response_data = {
                    'response': f"I'm having some technical difficulties right now. Please try again later. (Error: {str(e)})",
                    'agent_name': agent_type,
                    'status': 'error'
                }
            
            # Add metadata
            response_data.update({
                'agent_type': agent_type,
                'timestamp': timezone.now().isoformat(),
                'conversation_id': f"{agent_type}_{user_id}_{int(timezone.now().timestamp())}"
            })
            
            return JsonResponse(response_data)
            
        except Exception as e:
            return JsonResponse({
                'error': f'Chat processing failed: {str(e)}',
                'fallback_response': 'I apologize, but I encountered a technical issue. Please try again.'
            }, status=500)


@api_view(['GET'])
def agent_list_api(request):
    """API endpoint for agent list with capabilities"""
    agents = AgentProfile.objects.all()
    
    agent_data = []
    for agent in agents:
        # Get performance metrics
        metrics = AgentPerformanceMetrics.objects.filter(agent=agent).first()
        
        agent_info = {
            'id': agent.id,
            'agent_type': agent.agent_type,
            'name': agent.name,
            'description': agent.description,
            'intelligence_level': agent.intelligence_level,
            'emotional_intelligence': agent.emotional_intelligence,
            'creativity_score': agent.creativity_score,
            'is_active': agent.is_active,
            'capabilities': agent.capabilities,
            'personality_traits': agent.personality_traits,
            'performance_metrics': {
                'conversations': metrics.total_conversations if metrics else 0,
                'avg_rating': metrics.average_rating if metrics else 0,
                'satisfaction': metrics.user_satisfaction_score if metrics else 0,
                'learning_progress': metrics.learning_progress_score if metrics else 0
            } if metrics else None
        }
        agent_data.append(agent_info)
    
    return Response({
        'agents': agent_data,
        'total_count': len(agent_data),
        'active_count': sum(1 for agent in agent_data if agent['is_active'])
    })


@api_view(['POST'])
def agent_feedback_api(request):
    """Submit feedback for agent improvement"""
    try:
        data = request.data
        agent_id = data.get('agent_id')
        user_id = data.get('user_id', 1)
        rating = data.get('rating')  # 1-5 scale
        feedback_text = data.get('feedback', '')
        interaction_id = data.get('interaction_id')
        
        if not agent_id or rating is None:
            return Response({
                'error': 'Agent ID and rating are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        agent = get_object_or_404(AgentProfile, id=agent_id)
        
        # Create or update interaction
        interaction, created = UserAgentInteraction.objects.get_or_create(
            id=interaction_id if interaction_id else None,
            defaults={
                'agent': agent,
                'user_id': user_id,
                'interaction_type': 'feedback',
                'feedback_rating': rating,
                'feedback_text': feedback_text
            }
        )
        
        if not created:
            interaction.feedback_rating = rating
            interaction.feedback_text = feedback_text
            interaction.save()
        
        # Update performance metrics
        metrics, created = AgentPerformanceMetrics.objects.get_or_create(
            agent=agent,
            defaults={
                'total_conversations': 1,
                'positive_feedback_count': 1 if rating >= 4 else 0,
                'user_satisfaction_score': rating * 20,  # Convert to 100 scale
                'average_rating': rating
            }
        )
        
        if not created:
            # Update existing metrics
            metrics.total_conversations += 1
            if rating >= 4:
                metrics.positive_feedback_count += 1
            
            # Recalculate averages
            all_ratings = UserAgentInteraction.objects.filter(
                agent=agent, feedback_rating__isnull=False
            ).values_list('feedback_rating', flat=True)
            
            if all_ratings:
                metrics.average_rating = sum(all_ratings) / len(all_ratings)
                metrics.user_satisfaction_score = metrics.average_rating * 20
            
            metrics.save()
        
        # Trigger learning update (synchronous for now)
        try:
            AgentLearningEngine._update_learning_from_feedback(agent, rating, feedback_text)
        except Exception as learning_error:
            # Log the error but don't fail the feedback recording
            print(f"Learning update failed: {learning_error}")
        
        return Response({
            'success': True,
            'message': 'Feedback recorded successfully',
            'agent_performance': {
                'average_rating': metrics.average_rating,
                'total_conversations': metrics.total_conversations,
                'satisfaction_score': metrics.user_satisfaction_score
            }
        })
        
    except Exception as e:
        return Response({
            'error': f'Failed to record feedback: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def agent_analytics_api(request, agent_id):
    """Get detailed analytics for specific agent"""
    agent = get_object_or_404(AgentProfile, id=agent_id)
    
    # Time-based analytics
    now = timezone.now()
    last_week = now - timedelta(days=7)
    last_month = now - timedelta(days=30)
    
    # Conversation analytics
    weekly_conversations = UserAgentInteraction.objects.filter(
        agent=agent, created_at__gte=last_week
    ).count()
    
    monthly_conversations = UserAgentInteraction.objects.filter(
        agent=agent, created_at__gte=last_month
    ).count()
    
    # Rating distribution
    rating_distribution = UserAgentInteraction.objects.filter(
        agent=agent, feedback_rating__isnull=False
    ).values('feedback_rating').annotate(count=Count('feedback_rating'))
    
    # Learning progress
    learning_metrics = AgentLearningData.objects.filter(
        agent=agent
    ).order_by('-created_at').first()
    
    # Capability assessment
    capabilities = AgentCapability.objects.filter(agent=agent).values(
        'capability_type', 'proficiency_level'
    )
    
    # Memory usage
    memory_stats = ConversationMemory.objects.filter(agent=agent).aggregate(
        total_memories=Count('id'),
        avg_importance=Avg('importance_score')
    )
    
    analytics_data = {
        'agent_info': {
            'name': agent.name,
            'type': agent.agent_type,
            'intelligence_level': agent.intelligence_level,
            'emotional_intelligence': agent.emotional_intelligence,
            'creativity_score': agent.creativity_score
        },
        'conversation_metrics': {
            'weekly_conversations': weekly_conversations,
            'monthly_conversations': monthly_conversations,
            'total_conversations': UserAgentInteraction.objects.filter(agent=agent).count()
        },
        'rating_distribution': list(rating_distribution),
        'learning_metrics': {
            'success_rate': learning_metrics.success_rate if learning_metrics else 0,
            'improvement_rate': learning_metrics.improvement_rate if learning_metrics else 0,
            'adaptation_speed': agent.adaptation_speed
        },
        'capabilities': list(capabilities),
        'memory_stats': memory_stats,
        'performance_trends': {
            'last_updated': agent.last_interaction.isoformat() if agent.last_interaction else None,
            'learning_rate': agent.learning_rate,
            'version': agent.version
        }
    }
    
    return Response(analytics_data)


@login_required
def agent_training_view(request):
    """Agent training and customization interface"""
    if request.method == 'POST':
        # Handle training data submission
        agent_id = request.POST.get('agent_id')
        training_data = request.POST.get('training_data')
        
        agent = get_object_or_404(AgentProfile, id=agent_id)
        
        # Create learning data entry
        AgentLearningData.objects.create(
            agent=agent,
            training_data={'custom_training': training_data},
            learning_type='custom_training',
            success_rate=0.8  # Initial estimate
        )
        
        return JsonResponse({'success': True, 'message': 'Training data added'})
    
    agents = AgentProfile.objects.all()
    return render(request, 'agents/training.html', {'agents': agents})


# Utility functions for advanced features
def get_agent_recommendations(user_id: int) -> list:
    """Get personalized agent recommendations for user"""
    # Analyze user interaction patterns
    user_interactions = UserAgentInteraction.objects.filter(
        user_id=user_id
    ).values('agent__agent_type').annotate(
        interaction_count=Count('id'),
        avg_rating=Avg('feedback_rating')
    )
    
    # Recommend based on preferences and unused agents
    all_agents = AgentProfile.objects.filter(is_active=True)
    used_agents = {interaction['agent__agent_type'] for interaction in user_interactions}
    
    recommendations = []
    for agent in all_agents:
        if agent.agent_type not in used_agents:
            recommendations.append({
                'agent': agent,
                'recommendation_score': agent.intelligence_level + agent.emotional_intelligence,
                'reason': f"Perfect match for your interests in {', '.join(agent.capabilities[:3])}"
            })
    
    return sorted(recommendations, key=lambda x: x['recommendation_score'], reverse=True)[:5]
