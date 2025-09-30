from django.apps import AppConfig

class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'

    def ready(self):
        import tasks.signals
        # Ensure default groups exist (safe to call multiple times)
        try:
            from django.contrib.auth.models import Group
            for name in ['User', 'Admin', 'SuperAdmin']:
                Group.objects.get_or_create(name=name)
        except Exception:
            # avoid crashing during migrations or when DB is not ready
            pass