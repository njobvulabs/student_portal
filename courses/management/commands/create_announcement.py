from django.core.management.base import BaseCommand
from courses.models import Course, Announcement
from users.models import User

class Command(BaseCommand):
    help = 'Creates a dummy announcement for the first instructor/course'

    def add_arguments(self, parser):
        parser.add_argument('--title', default='Daily Update', help='Announcement title')
        parser.add_argument('--content', default='No announcement today', help='Announcement content')
        parser.add_argument('--course-id', type=int, help='Course ID (uses first course if omitted)')

    def handle(self, *args, **options):
        instructor = User.objects.filter(role='instructor').first()
        if not instructor:
            self.stdout.write(self.style.ERROR('No instructor found'))
            return

        if options['course_id']:
            course = Course.objects.filter(id=options['course_id']).first()
        else:
            course = Course.objects.first()

        if not course:
            self.stdout.write(self.style.ERROR('No course found'))
            return

        announcement = Announcement.objects.create(
            course=course,
            instructor=instructor,
            title=options['title'],
            content=options['content'],
            is_active=True
        )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created announcement "{announcement.title}"')
        ) 