from django.shortcuts import redirect, render, get_object_or_404
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

class CourseUpdateView(UpdateView):
    model = Course
    template_name = "administrator/course/create.html"
    form_class = CourseForm
    success_url = reverse_lazy('course_list')
    pk_url_kwarg = 'id'

def delete_course(request,id ):
    course= get_object_or_404(Course,id=id)
    course.delete()
    return redirect('course_list')
    

class StudentListView(ListView):
    model = Student
    template_name = "administrator/student/list.html"

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
            return redirect('student_list')
        else:
            context = {
                'form': form,
                'user_form': user_form,
            }
            return render(request, 'administrator/student/create.html', context)

# def update_student(request,id):
#     student=Student.objects.get(id=id)
#     if request.method == 'GET':
#         user_form = UserCreationFormWithoutPassword()
#         form = StudentCreationForm()
#         context = {
#             'form': form,
#             'user_form': user_form,
#         }
#         return render(request, 'administrator/student/create.html', context)
#     elif request.method == 'POST':
#         user_form = UserCreationFormWithoutPassword(request.POST)
#         form = StudentCreationForm(request.POST)
#         if user_form.is_valid() and form.is_valid():
#             user = user_form.save(commit=True)
            
#             user.save()
#             student = form.save(commit=True)
#             student.user = user
#             student.save()
#             return redirect('student_list')
#         else:
#             context = {
#                 'form': form,
#                 'user_form': user_form,
#             }
#             return render(request, 'administrator/student/create.html', context)




class StaffListView(ListView):
    model = Staff
    template_name = "administrator/staff/list.html"

def create_staff(request):
    if request.method == 'GET':
        user_form = UserCreationFormWithoutPassword()
        form = StaffCreationForm()
        context = {
            'form': form,
            'user_form': user_form,
        }
        return render(request, 'administrator/staff/create.html', context)
    elif request.method == 'POST':
        user_form = UserCreationFormWithoutPassword(request.POST)
        form = StaffCreationForm(request.POST)
        if user_form.is_valid() and form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(request.POST['teacher_id'])
            user.save()
            staff = form.save(commit=False)
            staff.user = user
            staff.save()
            return redirect('staff_list')
        else:
            context = {
                'form': form,
                'user_form': user_form,
            }
            return render(request, 'administrator/staff/create.html', context)


