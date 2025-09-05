from django.db import models
from django.contrib.auth.models import User
import json


class AgentProfile(models.Model):
    """Core agent profile with advanced capabilities"""
    
    AGENT_TYPES = [
        ('ai_girlfriend_luvie', 'AI Girlfriend Luvie'),
        ('ai_rapstar_flow', 'AI Rapstar Flow'),
        ('business_advisor_pro', 'Business Advisor Pro'),
        ('content_creator_ace', 'Content Creator Ace'),
        ('cypher_securibot', 'Cypher SecuriBot'),
        ('emo_ai_sensitive', 'Emo AI Sensitive'),
        ('emoai_emotional_sister', 'EmoAI Emotional Sister'),
        ('kiddieai_smart_kid', 'KiddieAI Smart Kid'),
        ('memoriaai_memory_brain', 'MemoriaAI Memory Brain'),
        ('rude_agent_serious', 'Rude Agent Serious'),
        ('stellar_astromaster', 'Stellar AstroMaster'),
        ('dramaqueen', 'DramaQueen 🎭'),
        ('brocode', 'BroCode 🤝'),
        ('crybaby', 'CryBaby 😢'),
        ('gossipguru', 'GossipGuru 🐍'),
        ('roastmaster', 'RoastMaster 🔥'),
        ('ipinfo_navigator', 'IPInfo Navigator'),
        ('claude_king', 'Claude King 👑'),
    ]
    
    agent_type = models.CharField(max_length=50, choices=AGENT_TYPES, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    personality_traits = models.JSONField(default=dict)
    capabilities = models.JSONField(default=list)
    learning_model = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Advanced AI Features
    intelligence_level = models.IntegerField(default=85)  # 0-100 scale
    emotional_intelligence = models.IntegerField(default=80)
    creativity_score = models.IntegerField(default=75)
    learning_rate = models.FloatField(default=0.1)
    adaptation_speed = models.FloatField(default=0.05)
    
    def __str__(self):
        return f"{self.name} ({self.agent_type})"


class UserAgentInteraction(models.Model):
    """Track user interactions for learning and personalization"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    agent = models.ForeignKey(AgentProfile, on_delete=models.CASCADE)
    conversation_id = models.CharField(max_length=100)
    message_content = models.TextField()
    agent_response = models.TextField()
    user_feedback = models.CharField(max_length=20, choices=[
        ('positive', 'Positive'),
        ('negative', 'Negative'),
        ('neutral', 'Neutral'),
    ], null=True, blank=True)
    interaction_type = models.CharField(max_length=50)  # chat, task, creative, etc.
    context_data = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'agent', 'timestamp']),
            models.Index(fields=['conversation_id']),
        ]


class AgentLearningData(models.Model):
    """Store learning patterns and improvements"""
    
    agent = models.ForeignKey(AgentProfile, on_delete=models.CASCADE)
    learning_session = models.CharField(max_length=100)
    input_pattern = models.TextField()
    output_pattern = models.TextField()
    success_rate = models.FloatField(default=0.0)
    improvement_metrics = models.JSONField(default=dict)
    training_data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)


class AgentCapability(models.Model):
    """Define specific capabilities for each agent"""
    
    agent = models.ForeignKey(AgentProfile, on_delete=models.CASCADE, related_name='agent_capabilities')
    capability_name = models.CharField(max_length=100)
    capability_type = models.CharField(max_length=50, choices=[
        ('communication', 'Communication'),
        ('analysis', 'Analysis'),
        ('creative', 'Creative'),
        ('technical', 'Technical'),
        ('emotional', 'Emotional'),
        ('learning', 'Learning'),
        ('memory', 'Memory'),
        ('specialized', 'Specialized'),
    ])
    proficiency_level = models.IntegerField(default=50)  # 0-100
    implementation_status = models.CharField(max_length=20, choices=[
        ('planned', 'Planned'),
        ('development', 'In Development'),
        ('testing', 'Testing'),
        ('active', 'Active'),
        ('optimizing', 'Optimizing'),
    ], default='planned')
    feature_details = models.JSONField(default=dict)
    
    class Meta:
        unique_together = ['agent', 'capability_name']


class ConversationMemory(models.Model):
    """Advanced memory system for each agent"""
    
    agent = models.ForeignKey(AgentProfile, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    memory_type = models.CharField(max_length=50, choices=[
        ('short_term', 'Short Term'),
        ('long_term', 'Long Term'),
        ('episodic', 'Episodic'),
        ('semantic', 'Semantic'),
        ('emotional', 'Emotional'),
        ('procedural', 'Procedural'),
    ])
    memory_content = models.JSONField()
    importance_score = models.FloatField(default=0.5)
    access_count = models.IntegerField(default=0)
    last_accessed = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['agent', 'user', 'importance_score']),
            models.Index(fields=['memory_type', 'last_accessed']),
        ]


class AgentPerformanceMetrics(models.Model):
    """Track agent performance and learning progress"""
    
    agent = models.ForeignKey(AgentProfile, on_delete=models.CASCADE)
    metric_date = models.DateField(auto_now_add=True)
    conversations_count = models.IntegerField(default=0)
    positive_feedback_rate = models.FloatField(default=0.0)
    response_accuracy = models.FloatField(default=0.0)
    learning_progress = models.FloatField(default=0.0)
    user_satisfaction = models.FloatField(default=0.0)
    task_completion_rate = models.FloatField(default=0.0)
    creativity_score = models.FloatField(default=0.0)
    adaptability_score = models.FloatField(default=0.0)
    
    class Meta:
        unique_together = ['agent', 'metric_date']
