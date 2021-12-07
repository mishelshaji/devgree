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

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'      


class EventssForm(ModelForm):
    class Meta:
        model = Eventss
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }     