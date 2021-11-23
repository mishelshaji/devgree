from django.forms import ModelForm
from .models import *

class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = '__all__'