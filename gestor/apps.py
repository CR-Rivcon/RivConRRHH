from django.apps import AppConfig


class GestorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestor'
    verbose_name = 'Sistema de Onboarding'
    
    def ready(self):
        """Importar signals cuando la app esté lista."""
        import gestor.models  # Esto cargará los signals definidos en models.py
