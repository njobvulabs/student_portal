from django.contrib import admin
from django.utils.html import format_html
from .models import Course, Enrollment, Grade, Announcement, Assignment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'instructor', 'is_active', 'student_count', 'actions_buttons')
    list_filter = ('is_active', 'instructor', 'created_at')
    search_fields = ('code', 'name', 'instructor__username', 'instructor__first_name', 'instructor__last_name')
    ordering = ('-created_at',)
    list_per_page = 20
    
    def student_count(self, obj):
        return obj.students.count()
    student_count.short_description = 'Enrolled Students'
    
    def actions_buttons(self, obj):
        return format_html(
            '<a class="button" href="{}">Edit</a>&nbsp;'
            '<a class="button" href="{}">Delete</a>',
            f'/admin/courses/course/{obj.id}/change/',
            f'/admin/courses/course/{obj.id}/delete/'
        )
    actions_buttons.short_description = 'Actions'
    actions_buttons.allow_tags = True

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'due_date', 'max_score', 'weight', 'is_active')
    list_filter = ('course', 'is_active', 'due_date')
    search_fields = ('title', 'course__code', 'course__name')
    ordering = ('due_date',)
    list_per_page = 20

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'course_code', 'assignment_title', 'score', 'submitted_at')
    list_filter = ('submitted_at', 'assignment__course', 'enrollment__student')
    search_fields = ('enrollment__student__username', 'enrollment__student__first_name', 'enrollment__student__last_name', 'assignment__title')
    ordering = ('-submitted_at',)
    list_per_page = 20
    
    def student_name(self, obj):
        return obj.enrollment.student.get_full_name()
    student_name.short_description = 'Student'
    
    def course_code(self, obj):
        return obj.enrollment.course.code
    course_code.short_description = 'Course'
    
    def assignment_title(self, obj):
        return obj.assignment.title
    assignment_title.short_description = 'Assignment'

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrollment_date', 'is_active')
    list_filter = ('is_active', 'enrollment_date', 'course')
    search_fields = ('student__username', 'student__first_name', 'student__last_name', 'course__code', 'course__name')
    ordering = ('-enrollment_date',)
    list_per_page = 20

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'instructor', 'created_at', 'expires_at', 'is_active')
    list_filter = ('is_active', 'course', 'instructor', 'created_at')
    search_fields = ('title', 'content', 'course__code', 'instructor__username')
    ordering = ('-created_at',)
    list_per_page = 20
