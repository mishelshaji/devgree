from django.forms import ModelForm
from django import forms
from .models import *
from accounts.models import User

class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = '__all__'

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

class UserCreationFormWithoutPassword(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class StudentCreationForm(ModelForm):
    class Meta:
        model = Student
        exclude = ['user']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }


class UserCreationFormWithoutPassword(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class StaffCreationForm(ModelForm):
    class Meta:
        model = Staff 
        exclude = ['user']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }