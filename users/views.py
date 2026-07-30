from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Avg
from django.db import models
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import os
from .models import User
from courses.models import Course, Enrollment, Announcement, Grade
from .forms import UserRegistrationForm, UserProfileForm

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html', {
        'title': 'Welcome to Student Portal',
        'description': 'Your one-stop platform for managing your academic journey.'
    })

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, 'Account created successfully! Welcome to Student Portal.')
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, 'An error occurred while creating your account. Please try again.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {
        'form': form,
        'title': 'Create Account',
        'description': 'Join our academic community'
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        
        if not username or not password:
            messages.error(request, 'Please provide both username and password.')
            return render(request, 'users/login.html')
        
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if not remember:
                    request.session.set_expiry(0)
                messages.success(request, f'Welcome back, {user.get_full_name()}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        except Exception as e:
            messages.error(request, 'An error occurred during login. Please try again.')
    
    return render(request, 'users/login.html', {
        'title': 'Login',
        'description': 'Access your student portal'
    })

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

@login_required
def dashboard(request):
    context = {
        'title': 'Dashboard',
        'description': 'Your academic overview'
    }
    
    if request.user.role == 'student':
        enrollments = Enrollment.objects.filter(student=request.user, is_active=True)
        context['enrolled_courses'] = enrollments
        
        # Calculate average grade across all assignments
        grades = Grade.objects.filter(enrollment__in=enrollments).select_related('assignment')
        if grades.exists():
            total_pct = 0
            count = 0
            for grade in grades:
                if grade.assignment and grade.assignment.max_score > 0:
                    total_pct += float(grade.score) / float(grade.assignment.max_score) * 100
                    count += 1
            context['average_grade'] = round(total_pct / count, 1) if count > 0 else None
        else:
            context['average_grade'] = None
            
        # Get announcements for enrolled courses
        announcements = Announcement.objects.filter(
            course__in=enrollments.values_list('course', flat=True),
            is_active=True
        )
        context['unread_announcements'] = announcements.exclude(read_by=request.user)
        context['recent_announcements'] = announcements.order_by('-created_at')[:5]

    elif request.user.role == 'instructor':
        teaching_courses = Course.objects.filter(instructor=request.user, is_active=True)
        context['teaching_courses'] = teaching_courses
        context['total_students'] = Enrollment.objects.filter(
            course__in=teaching_courses,
            is_active=True
        ).count()
        context['recent_announcements'] = Announcement.objects.filter(
            course__in=teaching_courses,
            is_active=True
        ).order_by('-created_at')[:5]

    return render(request, 'users/dashboard.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        action = request.POST.get('action', 'personal')

        if action == 'password':
            current = request.POST.get('current_password')
            new_pass = request.POST.get('new_password')
            confirm = request.POST.get('confirm_password')
            if request.user.check_password(current) and new_pass and new_pass == confirm:
                request.user.set_password(new_pass)
                request.user.save()
                messages.success(request, 'Password changed. Please log in again.')
                return redirect('login')
            else:
                messages.error(request, 'Password change failed. Check your input.')

        elif action == 'preferences':
            request.user.language = request.POST.get('language', 'en')
            request.user.timezone = request.POST.get('timezone', 'UTC')
            request.user.email_notifications = request.POST.get('email_notifications') == 'on'
            request.user.save()
            messages.success(request, 'Preferences saved!')

        else:
            form = UserProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                request.user.bio = request.POST.get('bio', '')
                request.user.save()
                messages.success(request, 'Profile updated successfully!')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
                return render(request, 'users/profile.html', {'form': form})

        return redirect('profile')

    form = UserProfileForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})



@user_passes_test(lambda u: u.is_admin())
def user_management(request):
    users = User.objects.all()
    return render(request, 'users/user_management.html', {'users': users})

@user_passes_test(lambda u: u.is_admin())
def create_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}')
            return redirect('user_management')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/create_user.html', {'form': form})

@login_required
@require_POST
def update_profile_picture(request):
    if 'profile_picture' not in request.FILES:
        return JsonResponse({'success': False, 'error': 'No file uploaded'})
    
    file = request.FILES['profile_picture']
    
    # Validate file type
    allowed_types = ['image/jpeg', 'image/png', 'image/gif']
    if file.content_type not in allowed_types:
        return JsonResponse({'success': False, 'error': 'Invalid file type'})
    
    # Validate file size (max 5MB)
    if file.size > 5 * 1024 * 1024:
        return JsonResponse({'success': False, 'error': 'File too large'})
    
    # Delete old profile picture if it exists
    if request.user.profile_picture:
        old_picture_path = request.user.profile_picture.path
        if os.path.exists(old_picture_path):
            os.remove(old_picture_path)
    
    # Save new profile picture
    request.user.profile_picture = file
    request.user.save()
    
    return JsonResponse({
        'success': True,
        'picture_url': request.user.profile_picture.url
    })

@login_required
@require_POST
def delete_profile_picture(request):
    if request.user.profile_picture:
        # Delete the file
        old_picture_path = request.user.profile_picture.path
        if os.path.exists(old_picture_path):
            os.remove(old_picture_path)
        
        # Clear the field
        request.user.profile_picture = None
        request.user.save()
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'No profile picture to delete'})
