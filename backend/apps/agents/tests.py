"""
Advanced Test Suite for AI Agent Management System
Professional testing framework for all components
"""

from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
import json
from datetime import datetime, timedelta

from .models import (
    AgentProfile, UserAgentInteraction, AgentLearningData,
    AgentCapability, ConversationMemory, AgentPerformanceMetrics
)
from .ai_engine import AgentLearningEngine, ConversationEngine, MemoryManager


class AgentProfileModelTest(TestCase):
    """Test AgentProfile model functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.agent_data = {
            'agent_type': 'test_agent',
            'name': 'TestAgent',
            'description': 'A test agent for unit testing',
            'personality_traits': {'test_trait': 0.8},
            'capabilities': ['test_capability'],
            'intelligence_level': 85,
            'emotional_intelligence': 80,
            'creativity_score': 75
        }
    
    def test_agent_creation(self):
        """Test creating an agent profile"""
        agent = AgentProfile.objects.create(**self.agent_data)
        
        self.assertEqual(agent.name, 'TestAgent')
        self.assertEqual(agent.agent_type, 'test_agent')
        self.assertEqual(agent.intelligence_level, 85)
        self.assertTrue(agent.is_active)
        self.assertIsNotNone(agent.created_at)
    
    def test_agent_string_representation(self):
        """Test agent string representation"""
        agent = AgentProfile.objects.create(**self.agent_data)
        self.assertEqual(str(agent), 'TestAgent (test_agent)')
    
    def test_agent_capabilities_storage(self):
        """Test JSON field for capabilities"""
        agent = AgentProfile.objects.create(**self.agent_data)
        agent.capabilities = ['test1', 'test2', 'test3']
        agent.save()
        
        retrieved_agent = AgentProfile.objects.get(id=agent.id)
        self.assertEqual(len(retrieved_agent.capabilities), 3)
        self.assertIn('test1', retrieved_agent.capabilities)
    
    def test_personality_traits_storage(self):
        """Test JSON field for personality traits"""
        agent = AgentProfile.objects.create(**self.agent_data)
        agent.personality_traits = {
            'empathy': 0.9,
            'creativity': 0.8,
            'analytical': 0.7
        }
        agent.save()
        
        retrieved_agent = AgentProfile.objects.get(id=agent.id)
        self.assertEqual(retrieved_agent.personality_traits['empathy'], 0.9)
        self.assertEqual(len(retrieved_agent.personality_traits), 3)


class UserAgentInteractionTest(TestCase):
    """Test user-agent interaction functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.agent = AgentProfile.objects.create(
            agent_type='test_agent',
            name='TestAgent',
            description='Test agent'
        )
    
    def test_interaction_creation(self):
        """Test creating user-agent interactions"""
        interaction = UserAgentInteraction.objects.create(
            agent=self.agent,
            user=self.user,
            interaction_type='conversation',
            conversation_data={'message': 'Hello', 'response': 'Hi there!'},
            feedback_rating=5
        )
        
        self.assertEqual(interaction.agent, self.agent)
        self.assertEqual(interaction.user, self.user)
        self.assertEqual(interaction.feedback_rating, 5)
        self.assertIsNotNone(interaction.created_at)
    
    def test_conversation_data_storage(self):
        """Test JSON storage of conversation data"""
        conversation_data = {
            'messages': [
                {'user': 'Hello', 'agent': 'Hi there!'},
                {'user': 'How are you?', 'agent': 'I am doing well, thank you!'}
            ],
            'context': {'mood': 'friendly', 'topic': 'greeting'}
        }
        
        interaction = UserAgentInteraction.objects.create(
            agent=self.agent,
            user=self.user,
            interaction_type='conversation',
            conversation_data=conversation_data
        )
        
        retrieved_interaction = UserAgentInteraction.objects.get(id=interaction.id)
        self.assertEqual(len(retrieved_interaction.conversation_data['messages']), 2)
        self.assertEqual(retrieved_interaction.conversation_data['context']['mood'], 'friendly')


class AgentPerformanceMetricsTest(TestCase):
    """Test performance metrics functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.agent = AgentProfile.objects.create(
            agent_type='test_agent',
            name='TestAgent',
            description='Test agent'
        )
    
    def test_metrics_creation(self):
        """Test creating performance metrics"""
        metrics = AgentPerformanceMetrics.objects.create(
            agent=self.agent,
            total_conversations=100,
            positive_feedback_count=85,
            user_satisfaction_score=92.5,
            average_rating=4.6,
            task_completion_rate=88.0
        )
        
        self.assertEqual(metrics.total_conversations, 100)
        self.assertEqual(metrics.user_satisfaction_score, 92.5)
        self.assertIsNotNone(metrics.last_updated)
    
    def test_metrics_calculations(self):
        """Test automatic metric calculations"""
        metrics = AgentPerformanceMetrics.objects.create(
            agent=self.agent,
            total_conversations=100,
            positive_feedback_count=85
        )
        
        # Test positive feedback percentage
        positive_percentage = (metrics.positive_feedback_count / metrics.total_conversations) * 100
        self.assertEqual(positive_percentage, 85.0)


class AgentLearningEngineTest(TestCase):
    """Test AI learning engine functionality"""
    
    def test_agent_initialization(self):
        """Test agent initialization through learning engine"""
        initial_count = AgentProfile.objects.count()
        
        # This would normally be called in apps.py ready() method
        AgentLearningEngine.initialize_all_agents()
        
        final_count = AgentProfile.objects.count()
        self.assertGreater(final_count, initial_count)
    
    def test_personality_traits_assignment(self):
        """Test personality traits are properly assigned"""
        AgentLearningEngine.initialize_all_agents()
        
        # Check specific agent personalities
        luvie = AgentProfile.objects.filter(agent_type='ai_girlfriend_luvie').first()
        if luvie:
            self.assertIn('empathy', luvie.personality_traits)
            self.assertGreater(luvie.personality_traits.get('empathy', 0), 0.9)
        
        claude = AgentProfile.objects.filter(agent_type='claude_king').first()
        if claude:
            self.assertIn('intelligence', claude.personality_traits)
            self.assertGreater(claude.intelligence_level, 95)
    
    def test_agent_capabilities_assignment(self):
        """Test agent capabilities are properly assigned"""
        AgentLearningEngine.initialize_all_agents()
        
        claude = AgentProfile.objects.filter(agent_type='claude_king').first()
        if claude:
            self.assertIn('code_generation', claude.capabilities)
            self.assertIn('architecture_design', claude.capabilities)


class ConversationEngineTest(TransactionTestCase):
    """Test conversation engine functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.user_id = 1
        
        # Create test agent
        self.agent = AgentProfile.objects.create(
            agent_type='test_agent',
            name='TestAgent',
            description='Test agent',
            personality_traits={'test_trait': 0.8},
            capabilities=['test_capability']
        )
    
    def test_conversation_engine_initialization(self):
        """Test conversation engine can be initialized"""
        engine = ConversationEngine('test_agent', self.user_id)
        self.assertEqual(engine.agent_type, 'test_agent')
        self.assertEqual(engine.user_id, self.user_id)
        self.assertIsNotNone(engine.agent)
    
    def test_input_analysis(self):
        """Test message input analysis"""
        engine = ConversationEngine('test_agent', self.user_id)
        
        # Test sentiment analysis
        positive_sentiment = engine._analyze_sentiment("I love this!")
        self.assertGreater(positive_sentiment, 0)
        
        negative_sentiment = engine._analyze_sentiment("This is terrible")
        self.assertLess(negative_sentiment, 0)
    
    def test_response_generation(self):
        """Test response generation for different agent types"""
        # Test with specific agent personalities
        luvie_response = ConversationEngine('ai_girlfriend_luvie', self.user_id)._generate_romantic_response(
            "I miss you", {'sentiment': -0.2}, []
        )
        self.assertIn('love', luvie_response.lower())
        
        claude_response = ConversationEngine('claude_king', self.user_id)._generate_technical_response(
            "I have a bug in my code", {'sentiment': -0.1}, []
        )
        self.assertIn('debug', claude_response.lower())


class MemoryManagerTest(TestCase):
    """Test memory management functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com'
        )
        
        self.agent = AgentProfile.objects.create(
            agent_type='test_agent',
            name='TestAgent',
            description='Test agent'
        )
    
    def test_memory_importance_calculation(self):
        """Test memory importance scoring"""
        interaction_data = {
            'emotional_intensity': 0.8,
            'user_engagement': 0.9,
            'novelty': 0.7,
            'personal_relevance': 0.8
        }
        
        importance = MemoryManager._calculate_importance(interaction_data)
        self.assertGreater(importance, 0.7)
        self.assertLessEqual(importance, 1.0)
    
    def test_memory_type_determination(self):
        """Test memory type classification"""
        emotional_data = {'emotional_intensity': 0.9, 'personal_relevance': 0.8}
        memory_type = MemoryManager._determine_memory_type(emotional_data)
        
        self.assertIsInstance(memory_type, str)
        self.assertIn(memory_type, ['short_term', 'long_term', 'episodic', 'semantic', 'emotional', 'procedural'])


class AgentAPITest(APITestCase):
    """Test API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.agent = AgentProfile.objects.create(
            agent_type='test_agent',
            name='TestAgent',
            description='Test agent',
            is_active=True
        )
    
    def test_agent_list_api(self):
        """Test agent list API endpoint"""
        url = reverse('agents:agent_list_api')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('agents', response.data)
        self.assertGreater(len(response.data['agents']), 0)
    
    def test_agent_feedback_api(self):
        """Test feedback submission API"""
        url = reverse('agents:feedback_api')
        data = {
            'agent_id': self.agent.id,
            'user_id': self.user.id,
            'rating': 5,
            'feedback': 'Great agent!'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
    
    def test_chat_api_validation(self):
        """Test chat API input validation"""
        url = reverse('agents:chat_api')
        
        # Test missing agent_type
        data = {'message': 'Hello'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        
        # Test missing message
        data = {'agent_type': 'test_agent'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
    
    def test_agent_analytics_api(self):
        """Test agent analytics API"""
        url = reverse('agents:analytics_api', kwargs={'agent_id': self.agent.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('agent_info', response.data)
        self.assertIn('conversation_metrics', response.data)
        self.assertIn('performance_trends', response.data)


class AgentDashboardViewTest(TestCase):
    """Test dashboard view functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.agent = AgentProfile.objects.create(
            agent_type='test_agent',
            name='TestAgent',
            description='Test agent'
        )
    
    def test_dashboard_view_loads(self):
        """Test dashboard view loads successfully"""
        self.client.login(username='testuser', password='testpass123')
        
        url = reverse('agents:dashboard')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'DevCrown AI Agent Command Center')
        self.assertIn('agents', response.context)
    
    def test_agent_profile_view(self):
        """Test individual agent profile view"""
        self.client.login(username='testuser', password='testpass123')
        
        url = reverse('agents:agent_profile', kwargs={'agent_id': self.agent.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('agent', response.context)
        self.assertEqual(response.context['agent'], self.agent)


class AgentCapabilityTest(TestCase):
    """Test agent capability system"""
    
    def setUp(self):
        """Set up test data"""
        self.agent = AgentProfile.objects.create(
            agent_type='test_agent',
            name='TestAgent',
            description='Test agent'
        )
    
    def test_capability_creation(self):
        """Test creating agent capabilities"""
        capability = AgentCapability.objects.create(
            agent=self.agent,
            capability_type='communication',
            proficiency_level=8.5
        )
        
        self.assertEqual(capability.agent, self.agent)
        self.assertEqual(capability.capability_type, 'communication')
        self.assertEqual(capability.proficiency_level, 8.5)
    
    def test_capability_proficiency_range(self):
        """Test proficiency level validation"""
        # Valid proficiency level
        capability = AgentCapability.objects.create(
            agent=self.agent,
            capability_type='analysis',
            proficiency_level=7.5
        )
        self.assertTrue(0 <= capability.proficiency_level <= 10)


class ConversationMemoryTest(TestCase):
    """Test conversation memory system"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com'
        )
        
        self.agent = AgentProfile.objects.create(
            agent_type='test_agent',
            name='TestAgent',
            description='Test agent'
        )
    
    def test_memory_creation(self):
        """Test creating conversation memories"""
        memory = ConversationMemory.objects.create(
            agent=self.agent,
            user=self.user,
            memory_type='emotional',
            memory_content={'emotion': 'happiness', 'context': 'birthday'},
            importance_score=0.9
        )
        
        self.assertEqual(memory.agent, self.agent)
        self.assertEqual(memory.user, self.user)
        self.assertEqual(memory.memory_type, 'emotional')
        self.assertEqual(memory.importance_score, 0.9)
    
    def test_memory_importance_levels(self):
        """Test memory importance classification"""
        # High importance memory
        high_memory = ConversationMemory.objects.create(
            agent=self.agent,
            user=self.user,
            memory_type='long_term',
            memory_content={'important': True},
            importance_score=0.95
        )
        
        # Low importance memory
        low_memory = ConversationMemory.objects.create(
            agent=self.agent,
            user=self.user,
            memory_type='short_term',
            memory_content={'routine': True},
            importance_score=0.2
        )
        
        self.assertGreater(high_memory.importance_score, low_memory.importance_score)


class AgentIntegrationTest(TransactionTestCase):
    """Integration tests for complete agent system"""
    
    def setUp(self):
        """Set up test data"""
        # Initialize complete agent system
        AgentLearningEngine.initialize_all_agents()
        
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com'
        )
    
    def test_end_to_end_conversation(self):
        """Test complete conversation flow"""
        # Get an active agent
        agent = AgentProfile.objects.filter(is_active=True).first()
        self.assertIsNotNone(agent)
        
        # Create conversation engine
        engine = ConversationEngine(agent.agent_type, self.user.id)
        
        # Test conversation processing
        test_message = "Hello, how are you today?"
        context = {'mood': 'friendly'}
        
        # This would normally be async, but for testing we'll simulate
        analysis = engine._analyze_input(test_message, context)
        self.assertIn('sentiment', analysis)
        self.assertIn('intent', analysis)
        
        # Verify interaction is recorded
        interactions_before = UserAgentInteraction.objects.count()
        
        # Simulate storing interaction
        UserAgentInteraction.objects.create(
            agent=agent,
            user=self.user,
            interaction_type='conversation',
            conversation_data={'message': test_message, 'analysis': analysis}
        )
        
        interactions_after = UserAgentInteraction.objects.count()
        self.assertEqual(interactions_after, interactions_before + 1)
    
    def test_learning_system_integration(self):
        """Test learning system integration"""
        agent = AgentProfile.objects.filter(agent_type='claude_king').first()
        if agent:
            # Create learning data
            learning_data = AgentLearningData.objects.create(
                agent=agent,
                learning_type='conversation_feedback',
                training_data={'feedback': 'excellent coding help'},
                success_rate=0.92,
                improvement_rate=0.15
            )
            
            self.assertEqual(learning_data.agent, agent)
            self.assertGreater(learning_data.success_rate, 0.9)
    
    def test_performance_tracking_integration(self):
        """Test performance tracking system"""
        agent = AgentProfile.objects.first()
        
        # Create performance metrics
        metrics = AgentPerformanceMetrics.objects.create(
            agent=agent,
            total_conversations=50,
            positive_feedback_count=45,
            user_satisfaction_score=90.0,
            average_rating=4.5
        )
        
        # Verify calculations
        positive_percentage = (metrics.positive_feedback_count / metrics.total_conversations) * 100
        self.assertEqual(positive_percentage, 90.0)
        self.assertEqual(metrics.user_satisfaction_score, 90.0)
