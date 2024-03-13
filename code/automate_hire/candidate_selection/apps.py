from django.apps import AppConfig

# from . import signals


class CandidateSelectionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'candidate_selection'

    def ready(self):
        import candidate_selection.signals
