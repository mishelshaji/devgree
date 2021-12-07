from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.
@login_required
def admin_home(request):
    return render(request, 'administrator/home.html')

class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    template_name = "administrator/department/list.html"

class DepartmentCreateView(LoginRequiredMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = "administrator/department/create.html"
    success_url = reverse_lazy('department_list')

class DepartmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Department
    template_name = "administrator/department/create.html"
    form_class = DepartmentForm
    success_url = reverse_lazy('department_list')
    pk_url_kwarg = 'id'

class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = "administrator/course/list.html"
    queryset = Course.objects.select_related('department').all()

class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = "administrator/course/create.html"
    success_url = reverse_lazy('course_list')

class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    template_name = "administrator/course/create.html"
    form_class = CourseForm
    success_url = reverse_lazy('course_list')
    pk_url_kwarg = 'id'

@login_required
def delete_course(request,id ):
    course= get_object_or_404(Course,id=id)
    course.delete()
    return redirect('course_list')
    

class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = "administrator/student/list.html"

@login_required
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

@login_required
def update_student(request,id):
    student=get_object_or_404(Student, id=id)
    if request.method == 'GET':
        user_form = UserCreationFormWithoutPassword(instance=student.user)
        form = StudentCreationForm(instance=student)
        context = {
            'form': form,
            'user_form': user_form,
        }
        return render(request, 'administrator/student/create.html', context)
    elif request.method == 'POST':
        user_form = UserCreationFormWithoutPassword(data=request.POST, instance=student.user)
        form = StudentCreationForm(data=request.POST, instance=student)
        if user_form.is_valid() and form.is_valid():
            user_form.save()
            form.save()
            return redirect('student_list')
        else:
            context = {
                'form': form,
                'user_form': user_form,
            }
            return render(request, 'administrator/student/create.html', context)

@login_required
def delete_student(request, id):
    student = get_object_or_404(User, id=id, student=True)
    student.delete()
    return redirect('student_list')

class StaffListView(LoginRequiredMixin, ListView):
    model = Staff
    template_name = "administrator/staff/list.html"

@login_required
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
            user.student = False
            user.admin = False
            user.staff = True
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

@login_required
def edit_staff(request, id):
    user = get_object_or_404(User, id=id, staff=True, admin=False)
    staff = get_object_or_404(Staff, user=user)
    if request.method == 'GET':
        user_form = UserCreationFormWithoutPassword(instance=user)
        form = StaffCreationForm(instance=staff)
        context = {
            'form': form,
            'user_form': user_form,
        }
        return render(request, 'administrator/staff/create.html', context)

    elif request.method == 'POST':
        user_form = UserCreationFormWithoutPassword(data=request.POST, instance=user)
        form = StaffCreationForm(data=request.POST, instance=staff)
        if user_form.is_valid() and form.is_valid():
            form.save()
            user_form.save()
            return redirect('staff_list')
        else:
            context = {
                'form': form,
                'user_form': user_form,
            }
            return render(request, 'administrator/staff/create.html', context)

@login_required
def delete_staff(request, id):
    student = get_object_or_404(User, id=id, staff=True, admin=False)
    student.delete()
    return redirect('staff_list')

class RoomListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = "administrator/room/list.html"
    queryset = Room.objects.all()

class RoomCreateView(LoginRequiredMixin, CreateView):
    model = Room
    form_class = RoomForm
    template_name = "administrator/room/create.html"
    success_url = reverse_lazy('room_list')

class RoomUpdateView(LoginRequiredMixin, UpdateView):
    model = Room
    template_name = "administrator/room/create.html"
    form_class = RoomForm
    success_url = reverse_lazy('room_list')
    pk_url_kwarg = 'id'

@login_required
def delete_room(request,id ):
    room= get_object_or_404(Room,id=id)
    room.delete()
    return redirect('room_list')

