from django.db import models
from users.models import User

class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='courses_taught')
    students = models.ManyToManyField(User, through='Enrollment', related_name='enrolled_courses')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'courses'

    def __str__(self):
        return f"{self.code} - {self.name}"

    def get_total_assignments(self):
        return self.assignments.count()

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField()
    max_score = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'assignments'
        ordering = ['due_date']

    def __str__(self):
        return f"{self.course.code} - {self.title}"

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'enrollments'
        unique_together = ['student', 'course']

    def get_current_grade(self):
        grades = self.grade_set.all()
        if not grades.exists():
            return 0
        
        total_score = sum(grade.score for grade in grades)
        total_max = sum(grade.max_score for grade in grades)
        
        if total_max == 0:
            return 0
            
        return round((total_score / total_max) * 100, 1)

class Grade(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=True)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'grades'
        unique_together = ['enrollment', 'assignment']

    def __str__(self):
        return f"{self.enrollment.student.get_full_name()} - {self.assignment.title if self.assignment else 'No Assignment'}"

class Announcement(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    read_by = models.ManyToManyField(User, related_name='read_announcements', blank=True)

    class Meta:
        db_table = 'announcements'
        ordering = ['-created_at']
