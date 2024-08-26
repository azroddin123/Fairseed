from django.apps import AppConfig


class DonorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'donors'
    
    def ready(self) -> None:
        import donors.models
