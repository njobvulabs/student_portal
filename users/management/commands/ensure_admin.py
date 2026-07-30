from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Ensures a default admin user exists (idempotent)'

    def add_arguments(self, parser):
        parser.add_argument('--username', default='admin')
        parser.add_argument('--password', default='admin4213!')
        parser.add_argument('--email', default='admin@njovu.edu')

    def handle(self, *args, **options):
        opts = {k: options[k] for k in ['username', 'password', 'email']}

        user = User.objects.filter(username=opts['username']).first()
        if user:
            if user.role != User.ADMIN or not user.is_superuser:
                user.role = User.ADMIN
                user.is_staff = True
                user.is_superuser = True
                user.set_password(opts['password'])
                user.save(update_fields=['role', 'is_staff', 'is_superuser', 'password'])
                self.stdout.write(self.style.SUCCESS(f'Existing user "{opts["username"]}" upgraded to admin'))
            else:
                self.stdout.write(self.style.WARNING(f'Admin "{opts["username"]}" already exists, skipping'))
            return

        User.objects.create_superuser(
            username=opts['username'],
            password=opts['password'],
            email=opts['email'],
            role=User.ADMIN,
        )
        self.stdout.write(self.style.SUCCESS(
            f'Default admin created: {opts["username"]} / {opts["password"]}'
        ))
