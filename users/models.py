from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    STUDENT = 'student'
    INSTRUCTOR = 'instructor'
    ADMIN = 'admin'
    
    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (INSTRUCTOR, 'Instructor'),
        (ADMIN, 'Administrator'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STUDENT)
    student_id = models.CharField(max_length=20, blank=True, null=True)
    program_of_study = models.CharField(max_length=100, blank=True, null=True)
    year_of_study = models.IntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=10, default='en')
    timezone = models.CharField(max_length=50, default='UTC')
    email_notifications = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'users'
        
    def is_student(self):
        return self.role == self.STUDENT
        
    def is_instructor(self):
        return self.role == self.INSTRUCTOR
        
    def is_admin(self):
        return self.role == self.ADMIN
        
    def get_completion_rate(self):
        """Calculate the student's overall course completion rate"""
        if not self.is_student():
            return 0
            
        from courses.models import Enrollment, Grade, Assignment
        enrollments = Enrollment.objects.filter(student=self, is_active=True)
        if not enrollments.exists():
            return 0
            
        total_assignments = Assignment.objects.filter(course__in=enrollments.values_list('course', flat=True), is_active=True).count()
        completed_assignments = Grade.objects.filter(enrollment__in=enrollments).count()
        
        if total_assignments == 0:
            return 0
            
        return int((completed_assignments / total_assignments) * 100)
