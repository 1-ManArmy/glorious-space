"""
Advanced Django REST Framework Serializers
Professional API data serialization for AI agents
"""

from rest_framework import serializers
from .models import (
    AgentProfile, UserAgentInteraction, AgentLearningData,
    AgentCapability, ConversationMemory, AgentPerformanceMetrics
)


class AgentProfileSerializer(serializers.ModelSerializer):
    """Comprehensive agent profile serialization"""
    
    total_conversations = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    satisfaction_score = serializers.SerializerMethodField()
    capability_count = serializers.SerializerMethodField()
    
    class Meta:
        model = AgentProfile
        fields = [
            'id', 'agent_type', 'name', 'description', 'personality_traits',
            'capabilities', 'learning_model', 'intelligence_level',
            'emotional_intelligence', 'creativity_score', 'learning_rate',
            'adaptation_speed', 'is_active', 'version', 'created_at',
            'last_interaction', 'total_conversations', 'average_rating',
            'satisfaction_score', 'capability_count'
        ]
        read_only_fields = ['created_at', 'last_interaction']
    
    def get_total_conversations(self, obj):
        """Get total conversation count"""
        return UserAgentInteraction.objects.filter(agent=obj).count()
    
    def get_average_rating(self, obj):
        """Get average user rating"""
        metrics = AgentPerformanceMetrics.objects.filter(agent=obj).first()
        return metrics.average_rating if metrics else 0.0
    
    def get_satisfaction_score(self, obj):
        """Get user satisfaction score"""
        metrics = AgentPerformanceMetrics.objects.filter(agent=obj).first()
        return metrics.user_satisfaction_score if metrics else 0.0
    
    def get_capability_count(self, obj):
        """Get number of capabilities"""
        return AgentCapability.objects.filter(agent=obj).count()


class UserAgentInteractionSerializer(serializers.ModelSerializer):
    """User interaction tracking serialization"""
    
    agent_name = serializers.CharField(source='agent.name', read_only=True)
    agent_type = serializers.CharField(source='agent.agent_type', read_only=True)
    duration_minutes = serializers.SerializerMethodField()
    
    class Meta:
        model = UserAgentInteraction
        fields = [
            'id', 'agent', 'agent_name', 'agent_type', 'user', 'interaction_type',
            'conversation_data', 'feedback_rating', 'feedback_text',
            'created_at', 'updated_at', 'duration_minutes'
        ]
    
    def get_duration_minutes(self, obj):
        """Calculate interaction duration in minutes"""
        if obj.updated_at and obj.created_at:
            delta = obj.updated_at - obj.created_at
            return round(delta.total_seconds() / 60, 2)
        return 0.0


class AgentCapabilitySerializer(serializers.ModelSerializer):
    """Agent capability assessment serialization"""
    
    proficiency_percentage = serializers.SerializerMethodField()
    improvement_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = AgentCapability
        fields = [
            'id', 'agent', 'capability_type', 'proficiency_level',
            'proficiency_percentage', 'improvement_rate', 'last_assessed'
        ]
    
    def get_proficiency_percentage(self, obj):
        """Convert proficiency to percentage"""
        return round(obj.proficiency_level * 10, 1)  # 0-10 scale to 0-100%
    
    def get_improvement_rate(self, obj):
        """Calculate improvement rate based on learning data"""
        # This would involve comparing historical proficiency levels
        return 5.2  # Placeholder - implement actual calculation


class ConversationMemorySerializer(serializers.ModelSerializer):
    """Conversation memory serialization"""
    
    agent_name = serializers.CharField(source='agent.name', read_only=True)
    memory_age_days = serializers.SerializerMethodField()
    importance_level = serializers.SerializerMethodField()
    
    class Meta:
        model = ConversationMemory
        fields = [
            'id', 'agent', 'agent_name', 'user', 'memory_type',
            'memory_content', 'importance_score', 'importance_level',
            'created_at', 'last_accessed', 'memory_age_days'
        ]
    
    def get_memory_age_days(self, obj):
        """Calculate memory age in days"""
        from django.utils import timezone
        delta = timezone.now() - obj.created_at
        return delta.days
    
    def get_importance_level(self, obj):
        """Convert importance score to level"""
        if obj.importance_score >= 0.8:
            return 'Critical'
        elif obj.importance_score >= 0.6:
            return 'High'
        elif obj.importance_score >= 0.4:
            return 'Medium'
        else:
            return 'Low'


class AgentPerformanceMetricsSerializer(serializers.ModelSerializer):
    """Performance metrics comprehensive serialization"""
    
    agent_name = serializers.CharField(source='agent.name', read_only=True)
    efficiency_score = serializers.SerializerMethodField()
    growth_rate = serializers.SerializerMethodField()
    performance_grade = serializers.SerializerMethodField()
    
    class Meta:
        model = AgentPerformanceMetrics
        fields = [
            'id', 'agent', 'agent_name', 'total_conversations',
            'positive_feedback_count', 'user_satisfaction_score',
            'average_rating', 'task_completion_rate', 'response_accuracy',
            'learning_progress_score', 'creativity_rating',
            'adaptability_score', 'efficiency_score', 'growth_rate',
            'performance_grade', 'last_updated'
        ]
    
    def get_efficiency_score(self, obj):
        """Calculate overall efficiency score"""
        factors = [
            obj.user_satisfaction_score / 100,
            obj.task_completion_rate / 100,
            obj.response_accuracy / 100,
            obj.average_rating / 5.0
        ]
        return round(sum(factors) / len(factors) * 100, 1)
    
    def get_growth_rate(self, obj):
        """Calculate growth rate based on learning progress"""
        return round(obj.learning_progress_score * 1.2, 1)  # Simplified calculation
    
    def get_performance_grade(self, obj):
        """Assign performance grade"""
        efficiency = self.get_efficiency_score(obj)
        if efficiency >= 90:
            return 'A+'
        elif efficiency >= 80:
            return 'A'
        elif efficiency >= 70:
            return 'B'
        elif efficiency >= 60:
            return 'C'
        else:
            return 'D'


class AgentLearningDataSerializer(serializers.ModelSerializer):
    """Learning data and progress serialization"""
    
    agent_name = serializers.CharField(source='agent.name', read_only=True)
    learning_efficiency = serializers.SerializerMethodField()
    progress_trend = serializers.SerializerMethodField()
    
    class Meta:
        model = AgentLearningData
        fields = [
            'id', 'agent', 'agent_name', 'learning_type', 'training_data',
            'success_rate', 'improvement_rate', 'learning_efficiency',
            'progress_trend', 'created_at'
        ]
    
    def get_learning_efficiency(self, obj):
        """Calculate learning efficiency score"""
        return round((obj.success_rate + obj.improvement_rate) / 2, 2)
    
    def get_progress_trend(self, obj):
        """Determine progress trend"""
        if obj.improvement_rate > 0.8:
            return 'Excellent'
        elif obj.improvement_rate > 0.6:
            return 'Good'
        elif obj.improvement_rate > 0.4:
            return 'Average'
        else:
            return 'Needs Improvement'


# Specialized serializers for complex operations
class AgentDashboardSerializer(serializers.Serializer):
    """Dashboard summary data serialization"""
    
    total_agents = serializers.IntegerField()
    active_agents = serializers.IntegerField()
    total_conversations = serializers.IntegerField()
    average_satisfaction = serializers.FloatField()
    top_performing_agents = AgentProfileSerializer(many=True)
    recent_interactions = UserAgentInteractionSerializer(many=True)
    system_health_score = serializers.FloatField()
    
    class Meta:
        fields = [
            'total_agents', 'active_agents', 'total_conversations',
            'average_satisfaction', 'top_performing_agents',
            'recent_interactions', 'system_health_score'
        ]


class ChatMessageSerializer(serializers.Serializer):
    """Chat message input/output serialization"""
    
    agent_type = serializers.CharField(max_length=50)
    message = serializers.CharField()
    user_id = serializers.IntegerField(required=False, default=1)
    context = serializers.JSONField(required=False, default=dict)
    response = serializers.CharField(read_only=True)
    emotional_state = serializers.CharField(read_only=True)
    confidence = serializers.FloatField(read_only=True)
    conversation_id = serializers.CharField(read_only=True)
    timestamp = serializers.DateTimeField(read_only=True)
    
    def validate_agent_type(self, value):
        """Validate agent type exists"""
        if not AgentProfile.objects.filter(agent_type=value, is_active=True).exists():
            raise serializers.ValidationError(f"Agent type '{value}' not found or inactive")
        return value


class AgentRecommendationSerializer(serializers.Serializer):
    """Agent recommendation serialization"""
    
    agent = AgentProfileSerializer()
    recommendation_score = serializers.FloatField()
    reason = serializers.CharField()
    compatibility_factors = serializers.JSONField()
    estimated_satisfaction = serializers.FloatField()
    
    class Meta:
        fields = [
            'agent', 'recommendation_score', 'reason',
            'compatibility_factors', 'estimated_satisfaction'
        ]
