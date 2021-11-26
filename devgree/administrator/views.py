from django.shortcuts import render
from django.views.generic import CreateView, ListView
from .models import *
from .forms import *
from django.urls import reverse_lazy

# Create your views here.
def admin_home(request):
    return render(request, 'administrator/home.html')

class DepartmentListView(ListView):
    model = Department
    template_name = "administrator/department/list.html"

class DepartmentCreateView(CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = "administrator/department/create.html"
    success_url = reverse_lazy('department_list')


class CourseListView(ListView):
    model = Course
    template_name = "administrator/course/list.html"
    queryset = Course.objects.select_related('department').all()

class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = "administrator/course/create.html"
    success_url = reverse_lazy('course_list')