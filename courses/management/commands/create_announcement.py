from django.core.management.base import BaseCommand
from courses.models import Course, Announcement
from users.models import User

class Command(BaseCommand):
    help = 'Creates a new announcement'

    def handle(self, *args, **options):
        instructor = User.objects.filter(role='instructor').first()
        course = Course.objects.first()
        
        if not instructor:
            self.stdout.write(self.style.ERROR('No instructor found'))
            return
        
        if not course:
            self.stdout.write(self.style.ERROR('No course found'))
            return
        
        announcement = Announcement.objects.create(
            course=course,
            instructor=instructor,
            title='Daily Update',
            content='No announcement today',
            is_active=True
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created announcement "{announcement.title}"')
        ) 