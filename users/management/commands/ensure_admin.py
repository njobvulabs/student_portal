from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates a default admin user if none exists'

    def add_arguments(self, parser):
        parser.add_argument('--username', default='admin')
        parser.add_argument('--password', default='admin4213!')
        parser.add_argument('--email', default='admin@njovu.edu')

    def handle(self, *args, **options):
        if User.objects.filter(role=User.ADMIN).exists():
            self.stdout.write(self.style.WARNING('Admin user already exists, skipping'))
            return

        User.objects.create_superuser(
            username=options['username'],
            password=options['password'],
            email=options['email'],
            role=User.ADMIN,
        )
        self.stdout.write(self.style.SUCCESS(
            f'Default admin created: {options["username"]} / {options["password"]}'
        ))
