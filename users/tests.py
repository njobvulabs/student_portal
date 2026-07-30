from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(
            username='student1', password='testpass123', role=User.STUDENT
        )
        self.instructor = User.objects.create_user(
            username='instr1', password='testpass123', role=User.INSTRUCTOR
        )
        self.admin_user = User.objects.create_user(
            username='admin1', password='testpass123', role=User.ADMIN
        )

    def test_role_methods(self):
        self.assertTrue(self.student.is_student())
        self.assertFalse(self.student.is_instructor())
        self.assertFalse(self.student.is_admin())
        self.assertTrue(self.instructor.is_instructor())
        self.assertTrue(self.admin_user.is_admin())

    def test_completion_rate_zero_when_not_student(self):
        self.assertEqual(self.instructor.get_completion_rate(), 0)

    def test_str(self):
        self.student.first_name = 'Test'
        self.student.last_name = 'User'
        self.student.save()
        self.assertEqual(str(self.student), self.student.username)


class AuthViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_home_redirects_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('dashboard'))

    def test_home_anonymous(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_view_post_success(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser', 'password': 'testpass123'
        })
        self.assertRedirects(response, reverse('dashboard'))

    def test_login_view_post_fail(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser', 'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)

    def test_register_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertNotEqual(response.status_code, 200)

    def test_dashboard_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

    def test_profile_requires_login(self):
        response = self.client.get(reverse('profile'))
        self.assertNotEqual(response.status_code, 200)

    def test_profile_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
