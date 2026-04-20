from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'student_id', 'program_of_study', 'year_of_study',
            'phone_number', 'password1', 'password2'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make fields required
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['student_id'].required = True
        self.fields['program_of_study'].required = True
        self.fields['year_of_study'].required = True
        
        # Add help texts
        self.fields['username'].help_text = 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
        self.fields['email'].help_text = 'Required. Enter a valid email address.'
        self.fields['password1'].help_text = 'Your password must contain at least 8 characters.'
        
        # Add placeholders
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter your username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter your email'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Enter your first name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Enter your last name'})
        self.fields['phone_number'].widget.attrs.update({'placeholder': 'Enter your phone number'})
        self.fields['student_id'].widget.attrs.update({'placeholder': 'Enter your student ID'})
        self.fields['program_of_study'].widget.attrs.update({'placeholder': 'Enter your program of study'})
        self.fields['year_of_study'].widget.attrs.update({'placeholder': 'Enter your year of study'})

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.STUDENT  # Explicitly set role to student
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email',
            'phone_number', 'program_of_study', 'year_of_study'
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        
        # Add placeholders
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Enter your first name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Enter your last name'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter your email'})
        self.fields['phone_number'].widget.attrs.update({'placeholder': 'Enter your phone number'})
        
        # Make fields optional for non-student users
        if self.instance and self.instance.role != 'student':
            self.fields['program_of_study'].required = False
            self.fields['year_of_study'].required = False

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number']
        if User.role == User.STUDENT:
            fields.extend(['program_of_study', 'year_of_study'])
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})