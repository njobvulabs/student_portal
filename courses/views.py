from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Avg, Q
from .models import Course, Enrollment, Grade, Announcement
from .forms import CourseForm, GradeForm, AnnouncementForm
from users.models import User

@login_required
def course_list(request):
    if request.user.role == 'student':
        courses = Course.objects.filter(
            enrollment__student=request.user,
            enrollment__is_active=True,
            is_active=True
        )
    elif request.user.role == 'instructor':
        courses = Course.objects.filter(instructor=request.user, is_active=True)
    else:
        courses = Course.objects.filter(is_active=True)
    
    return render(request, 'courses/course_list.html', {
        'courses': courses,
        'title': 'Courses',
        'description': 'Browse available courses'
    })

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.user.role == 'student':
        enrollment = get_object_or_404(Enrollment, student=request.user, course=course)
        grades = Grade.objects.filter(enrollment=enrollment)
        context = {
            'course': course,
            'enrollment': enrollment,
            'grades': grades,
            'announcements': Announcement.objects.filter(course=course, is_active=True)
        }
    else:
        context = {
            'course': course,
            'students': course.students.filter(enrollment__is_active=True),
            'announcements': Announcement.objects.filter(course=course, is_active=True)
        }
    
    context.update({
        'title': f'Course: {course.name}',
        'description': course.description
    })
    
    return render(request, 'courses/course_detail.html', context)

@user_passes_test(lambda u: u.is_admin())
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            messages.success(request, f'Course {course.code} has been created.')
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form, 'action': 'Create'})

@login_required
@user_passes_test(lambda u: u.is_instructor())
def add_grade(request, course_id, student_id):
    course = get_object_or_404(Course, id=course_id)
    student = get_object_or_404(User, id=student_id)
    enrollment = get_object_or_404(Enrollment, course=course, student=student)
    
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.enrollment = enrollment
            grade.save()
            messages.success(request, 'Grade has been added successfully.')
            return redirect('course_detail', course_id=course_id)
    else:
        form = GradeForm()
    
    return render(request, 'courses/grade_form.html', {
        'form': form,
        'course': course,
        'student': student
    })

@login_required
@user_passes_test(lambda u: u.is_instructor())
def create_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.instructor = request.user
            announcement.save()
            messages.success(request, 'Announcement created successfully!')
            return redirect('courses:course_detail', course_id=announcement.course.id)
    else:
        form = AnnouncementForm(initial={'course': request.GET.get('course')})
        form.fields['course'].queryset = Course.objects.filter(instructor=request.user)
    
    return render(request, 'courses/create_announcement.html', {
        'form': form,
        'title': 'Create Announcement',
        'description': 'Create a new announcement for your course'
    })

@login_required
def announcement_list(request):
    if request.user.role == 'student':
        announcements = Announcement.objects.filter(
            course__enrollment__student=request.user,
            course__enrollment__is_active=True,
            is_active=True
        )
        # Add read status for each announcement
        for announcement in announcements:
            announcement.is_read = announcement.read_by.filter(id=request.user.id).exists()
    elif request.user.role == 'instructor':
        announcements = Announcement.objects.filter(
            course__instructor=request.user,
            is_active=True
        )
    else:
        announcements = Announcement.objects.filter(is_active=True)
    
    return render(request, 'courses/announcement_list.html', {
        'announcements': announcements,
        'title': 'Announcements',
        'description': 'View all announcements'
    })

@login_required
def announcement_detail(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    
    # Mark announcement as read for the current user
    if request.user.role == 'student':
        announcement.read_by.add(request.user)
    
    return render(request, 'courses/announcement_detail.html', {
        'announcement': announcement,
        'title': announcement.title,
        'description': f'Posted in {announcement.course.name}'
    })

@login_required
def grade_list(request):
    if request.user.role != 'student':
        messages.error(request, 'Only students can view grades.')
        return redirect('dashboard')
    
    enrollments = Enrollment.objects.filter(student=request.user, is_active=True)
    grades = Grade.objects.filter(enrollment__in=enrollments)
    
    # Calculate course averages
    course_averages = {}
    for enrollment in enrollments:
        course_grades = grades.filter(enrollment=enrollment)
        if course_grades.exists():
            avg = course_grades.annotate(
                percentage=(models.F('score') * 100.0 / models.F('max_score'))
            ).aggregate(avg=Avg('percentage'))['avg']
            course_averages[enrollment.course.id] = round(avg, 1) if avg else None
    
    return render(request, 'courses/grade_list.html', {
        'enrollments': enrollments,
        'grades': grades,
        'course_averages': course_averages,
        'title': 'Grades',
        'description': 'View your academic performance'
    })

@login_required
@user_passes_test(lambda u: u.is_student())
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # Check if already enrolled
    if Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.warning(request, f'You are already enrolled in {course.code}.')
        return redirect('courses:course_list')
    
    # Create enrollment
    Enrollment.objects.create(
        student=request.user,
        course=course,
        is_active=True
    )
    
    messages.success(request, f'Successfully enrolled in {course.code}.')
    return redirect('courses:course_detail', course_id=course.id)

@login_required
def available_courses(request):
    if request.user.role != 'student':
        messages.error(request, 'Only students can view available courses.')
        return redirect('dashboard')
    
    # Get courses the student is not enrolled in
    enrolled_courses = Course.objects.filter(
        enrollment__student=request.user,
        enrollment__is_active=True
    )
    available_courses = Course.objects.filter(
        is_active=True
    ).exclude(
        id__in=enrolled_courses.values_list('id', flat=True)
    )
    
    return render(request, 'courses/available_courses.html', {
        'courses': available_courses,
        'title': 'Available Courses',
        'description': 'Browse and enroll in available courses'
    })

@login_required
@user_passes_test(lambda u: u.is_admin)
def manage_courses(request):
    courses = Course.objects.all().order_by('-created_at')
    return render(request, 'courses/manage_courses.html', {
        'courses': courses,
        'title': 'Manage Courses',
        'description': 'Add, edit, or delete courses'
    })

@login_required
@user_passes_test(lambda u: u.is_admin)
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f'Course {course.code} has been updated.')
            return redirect('courses:manage_courses')
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'courses/course_form.html', {
        'form': form,
        'course': course,
        'title': f'Edit Course: {course.code}',
        'description': 'Update course details',
        'action': 'Update'
    })

@login_required
@user_passes_test(lambda u: u.is_admin)
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        course.delete()
        messages.success(request, f'Course {course.code} has been deleted.')
        return redirect('courses:manage_courses')
    
    return render(request, 'courses/delete_course.html', {
        'course': course,
        'title': f'Delete Course: {course.code}',
        'description': 'Are you sure you want to delete this course?'
    })
