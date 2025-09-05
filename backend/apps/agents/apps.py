from django.apps import AppConfig


class AgentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.apps.agents'
    
    def ready(self):
        """Initialize agent learning systems when Django starts"""
        from .ai_engine import AgentLearningEngine
        AgentLearningEngine.initialize_all_agents()
