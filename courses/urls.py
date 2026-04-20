from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('announcements/', views.announcement_list, name='announcements'),
    path('announcements/create/', views.create_announcement, name='create_announcement'),
    path('announcements/<int:announcement_id>/', views.announcement_detail, name='announcement_detail'),
    path('grades/', views.grade_list, name='grades'),
    path('available/', views.available_courses, name='available_courses'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('manage/', views.manage_courses, name='manage_courses'),
    path('manage/create/', views.create_course, name='create_course'),
    path('manage/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('manage/<int:course_id>/delete/', views.delete_course, name='delete_course'),
]
