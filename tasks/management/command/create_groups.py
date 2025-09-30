from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = "Create default groups: User, Admin, SuperAdmin"

    def handle(self, *args, **options):
        groups = ['User', 'Admin', 'SuperAdmin']
        for g in groups:
            group, created = Group.objects.get_or_create(name=g)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created group: {g}"))
            else:
                self.stdout.write(self.style.NOTICE(f"Group already exists: {g}"))
