from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Course, Enrollment, Grade, Assignment, Announcement

User = get_user_model()


class CourseModelTests(TestCase):
    def setUp(self):
        self.instructor = User.objects.create_user(
            username='instr', password='pass', role=User.INSTRUCTOR
        )
        self.course = Course.objects.create(
            code='CS101', name='Intro to CS', instructor=self.instructor
        )

    def test_course_str(self):
        self.assertEqual(str(self.course), 'CS101 - Intro to CS')

    def test_get_total_assignments(self):
        self.assertEqual(self.course.get_total_assignments(), 0)


class AssignmentModelTests(TestCase):
    def setUp(self):
        instructor = User.objects.create_user(username='i', password='p', role=User.INSTRUCTOR)
        course = Course.objects.create(code='MATH101', name='Calculus', instructor=instructor)
        self.assignment = Assignment.objects.create(
            course=course, title='Midterm', due_date='2026-12-31T23:59:59Z',
            max_score=100, weight=1.0
        )

    def test_assignment_str(self):
        self.assertEqual(str(self.assignment), 'MATH101 - Midterm')


class GradePropertyTests(TestCase):
    def setUp(self):
        instructor = User.objects.create_user(username='i', password='p', role=User.INSTRUCTOR)
        student = User.objects.create_user(username='s', password='p', role=User.STUDENT)
        course = Course.objects.create(code='PHY101', name='Physics', instructor=instructor)
        assignment = Assignment.objects.create(
            course=course, title='Quiz 1', due_date='2026-12-31T23:59:59Z',
            max_score=50, weight=1.0
        )
        enrollment = Enrollment.objects.create(student=student, course=course)
        self.grade = Grade.objects.create(enrollment=enrollment, assignment=assignment, score=42)

    def test_max_score_property(self):
        self.assertEqual(float(self.grade.max_score), 50.0)

    def test_assignment_name_property(self):
        self.assertEqual(self.grade.assignment_name, 'Quiz 1')


class EnrollmentModelTests(TestCase):
    def setUp(self):
        instructor = User.objects.create_user(username='i', password='p', role=User.INSTRUCTOR)
        student = User.objects.create_user(username='s', password='p', role=User.STUDENT)
        course = Course.objects.create(code='CHEM101', name='Chemistry', instructor=instructor)
        self.enrollment = Enrollment.objects.create(student=student, course=course)

    def test_get_current_grade_zero_when_no_grades(self):
        self.assertEqual(self.enrollment.get_current_grade(), 0)


class CourseViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.instructor = User.objects.create_user(
            username='instr', password='pass', role=User.INSTRUCTOR
        )
        self.student = User.objects.create_user(
            username='stu', password='pass', role=User.STUDENT
        )
        self.course = Course.objects.create(
            code='ENG101', name='English', instructor=self.instructor
        )

    def test_course_list_requires_login(self):
        response = self.client.get(reverse('courses:course_list'))
        self.assertNotEqual(response.status_code, 200)

    def test_course_list_student(self):
        self.client.login(username='stu', password='pass')
        response = self.client.get(reverse('courses:course_list'))
        self.assertEqual(response.status_code, 200)

    def test_course_detail_student_not_enrolled(self):
        self.client.login(username='stu', password='pass')
        response = self.client.get(reverse('courses:course_detail', args=[self.course.id]))
        self.assertEqual(response.status_code, 404)

    def test_enroll_course(self):
        self.client.login(username='stu', password='pass')
        response = self.client.get(reverse('courses:enroll_course', args=[self.course.id]))
        self.assertRedirects(response, reverse('courses:course_detail', args=[self.course.id]))

    def test_available_courses(self):
        self.client.login(username='stu', password='pass')
        response = self.client.get(reverse('courses:available_courses'))
        self.assertEqual(response.status_code, 200)

    def test_announcements(self):
        self.client.login(username='stu', password='pass')
        response = self.client.get(reverse('courses:announcements'))
        self.assertEqual(response.status_code, 200)

    def test_grades_requires_student(self):
        self.client.login(username='instr', password='pass')
        response = self.client.get(reverse('courses:grades'))
        self.assertRedirects(response, reverse('dashboard'))
