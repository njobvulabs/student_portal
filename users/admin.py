from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'actions_buttons')
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'student_id')
    ordering = ('-date_joined',)
    list_per_page = 20
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Student info', {'fields': ('student_id', 'program_of_study', 'year_of_study')}),
        ('Contact info', {'fields': ('phone_number',)}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    def actions_buttons(self, obj):
        return format_html(
            '<a class="button" href="{}">Edit</a>&nbsp;'
            '<a class="button" href="{}">Delete</a>',
            f'/admin/users/user/{obj.id}/change/',
            f'/admin/users/user/{obj.id}/delete/'
        )
    actions_buttons.short_description = 'Actions'
    actions_buttons.allow_tags = True
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj and obj.role != 'student':
            # Remove student-specific fields for non-student users
            fieldsets = tuple(fs for fs in fieldsets if fs[0] != 'Student info')
        return fieldsets
