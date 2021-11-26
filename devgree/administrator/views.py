from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
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


class DepartmentUpdateView(UpdateView):
    model = Department
    template_name = "administrator/department/create.html"
    form_class = DepartmentForm
    success_url = reverse_lazy('department_list')
    pk_url_kwarg = 'id'

class CourseListView(ListView):
    model = Course
    template_name = "administrator/course/list.html"
    queryset = Course.objects.select_related('department').all()

class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = "administrator/course/create.html"
    success_url = reverse_lazy('course_list')

def create_student(request):
    if request.method == 'GET':
        user_form = UserCreationFormWithoutPassword()
        form = StudentCreationForm()
        context = {
            'form': form,
            'user_form': user_form,
        }
        return render(request, 'administrator/student/create.html', context)
    elif request.method == 'POST':
        user_form = UserCreationFormWithoutPassword(request.POST)
        form = StudentCreationForm(request.POST)
        if user_form.is_valid() and form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(request.POST['register_number'])
            user.save()
            student = form.save(commit=False)
            student.user = user
            student.save()
        else:
            context = {
                'form': form,
                'user_form': user_form,
            }
            return render(request, 'administrator/student/create.html', context)

