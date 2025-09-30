from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Create default groups: User, Admin, SuperAdmin'

    def handle(self, *args, **options):
        for name in ['User', 'Admin', 'SuperAdmin']:
            group, created = Group.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created group: {name}'))
            else:
                self.stdout.write(f'Group already exists: {name}')
