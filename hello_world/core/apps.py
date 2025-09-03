# 👑 Core Application Configuration - Royal Settings
from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hello_world.core'
    verbose_name = '👑 Core Kingdom Features'
    
    def ready(self):
        """Initialize our royal kingdom when Django starts"""
        try:
            import hello_world.core.signals  # noqa
        except ImportError:
            pass
