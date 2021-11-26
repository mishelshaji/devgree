from django.forms import ModelForm
from .models import *

class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = '__all__'




class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'