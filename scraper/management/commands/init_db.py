from django.core.management.base import BaseCommand
from django.core.management import execute_from_command_line
import sys

class Command(BaseCommand):
    help = 'Initialize database with migrations'

    def handle(self, *args, **options):
        try:
            self.stdout.write('Running migrations...')
            execute_from_command_line(['manage.py', 'migrate'])
            self.stdout.write(
                self.style.SUCCESS('Database initialized successfully!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error initializing database: {e}')
            )
            sys.exit(1)
