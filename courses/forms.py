from django import forms
from .models import Course, Grade, Announcement, Assignment

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'name', 'description', 'instructor']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['assignment', 'score']
        widgets = {
            'score': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.enrollment = kwargs.pop('enrollment', None)
        super().__init__(*args, **kwargs)
        
        if self.enrollment:
            self.fields['assignment'].queryset = Assignment.objects.filter(
                course=self.enrollment.course,
                is_active=True
            )
        
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
    
    def clean(self):
        cleaned_data = super().clean()
        assignment = cleaned_data.get('assignment')
        score = cleaned_data.get('score')
        
        if assignment and score:
            if score > assignment.max_score:
                raise forms.ValidationError(f"Score cannot exceed maximum score of {assignment.max_score}")
        
        return cleaned_data

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date', 'max_score', 'weight']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'max_score': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'weight': forms.NumberInput(attrs={'step': '0.01', 'min': '0'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'expires_at']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
            'expires_at': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'}) 