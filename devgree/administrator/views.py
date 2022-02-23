from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils import timezone
import time
import datetime

# Create your views here.
@login_required
@user_passes_test(lambda u: u.admin)
def admin_home(request):
    context = {
        'students_count': Student.objects.count(),
        'departments_count': Department.objects.count(),
        'courses_count': Course.objects.count(),
        'staff_count': User.objects.filter(staff=True).count(),
        'contact_requests': Contact.objects.all(),
    }
    return render(request, 'administrator/home.html', context)

class DepartmentListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Department
    template_name = "administrator/department/list.html"

    def test_func(self):
        return self.request.user.admin

class DepartmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = "administrator/department/create.html"
    success_url = reverse_lazy('department_list')

    def test_func(self):
        return self.request.user.admin

class DepartmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Department
    template_name = "administrator/department/create.html"
    form_class = DepartmentForm
    success_url = reverse_lazy('department_list')
    pk_url_kwarg = 'id'

    def test_func(self):
        return self.request.user.admin

class CourseListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Course
    template_name = "administrator/course/list.html"
    queryset = Course.objects.select_related('department').all()

    def test_func(self):
        return self.request.user.admin

class CourseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = "administrator/course/create.html"
    success_url = reverse_lazy('course_list')

    def test_func(self):
        return self.request.user.admin

class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Course
    template_name = "administrator/course/create.html"
    form_class = CourseForm
    success_url = reverse_lazy('course_list')
    pk_url_kwarg = 'id'

    def test_func(self):
        return self.request.user.admin

@login_required
@user_passes_test(lambda u: u.admin)
def delete_course(request, id):
    course= get_object_or_404(Course,id=id)
    course.delete()
    return redirect('course_list')
    
class StudentListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Student
    template_name = "administrator/student/list.html"

    def get_queryset(self):
        queryset = Student.objects.select_related('user')
        search = self.request.GET.get('s', None)
        if search:
            queryset = queryset.filter(Q(user__email__icontains=search) | Q(register_number__icontains=search) | Q(roll_number__icontains=search))
        return queryset

    def test_func(self):
        return self.request.user.admin or self.request.user.staff

@login_required
@user_passes_test(lambda u: u.admin or u.staff)
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
        form = StudentCreationForm(request.POST, files=request.FILES)
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
@user_passes_test(lambda u: u.admin or u.staff)
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
        form = StudentCreationForm(data=request.POST, instance=student, files=request.FILES)
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
@user_passes_test(lambda u: u.admin or u.staff)
def delete_student(request, id):
    student = get_object_or_404(User, id=id, student=True)
    student.delete()
    return redirect('student_list')

class StaffListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Staff
    template_name = "administrator/staff/list.html"
    queryset = Staff.objects.select_related('user')

    def test_func(self):
        return self.request.user.admin

@login_required
@user_passes_test(lambda u: u.admin)
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
@user_passes_test(lambda u: u.admin)
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
@user_passes_test(lambda u: u.admin)
def delete_staff(request, id):
    student = get_object_or_404(User, id=id, staff=True, admin=False)
    student.delete()
    return redirect('staff_list')

class RoomListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Room
    template_name = "administrator/room/list.html"
    queryset = Room.objects.all()

    def test_func(self):
        return self.request.user.admin or self.request.user.staff

class RoomCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Room
    form_class = RoomForm
    template_name = "administrator/room/create.html"
    success_url = reverse_lazy('room_list')

    def test_func(self):
        return self.request.user.admin

class RoomUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Room
    template_name = "administrator/room/create.html"
    form_class = RoomForm
    success_url = reverse_lazy('room_list')
    pk_url_kwarg = 'id'

    def test_func(self):
        return self.request.user.admin

@login_required
@user_passes_test(lambda u: u.admin or u.staff)
def delete_room(request, id):
    room= get_object_or_404(Room,id=id)
    room.delete()
    return redirect('room_list')

class EventListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Event
    template_name = "administrator/event/list.html"
    queryset = Event.objects.select_related('department').all()

    def test_func(self):
        return self.request.user.admin or self.request.user.staff

class EventCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "administrator/event/create.html"
    success_url = reverse_lazy('event_list')

    def test_func(self):
        return self.request.user.admin or self.request.user.staff

class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    template_name = "administrator/event/create.html"
    form_class = EventForm
    success_url = reverse_lazy('event_list')
    pk_url_kwarg = 'id'

    def test_func(self):
        return self.request.user.admin or self.request.user.staff

@login_required
@user_passes_test(lambda u: u.admin or u.staff)
def delete_event(request,id ):
    event= get_object_or_404(Event,id=id)
    event.delete()
    return redirect('event_list')
    
class BookingListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Booking
    template_name = "administrator/booking/list.html"
    queryset = Booking.objects.select_related('room', 'event').filter(booked_from__gt= timezone.now())

    def test_func(self):
        return self.request.user.admin or self.request.user.staff

class BookingCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = "administrator/booking/create.html"
    success_url = reverse_lazy('booking_list')

    def test_func(self):
        return self.request.user.admin or self.request.user.staff

class BookingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Booking
    template_name = "administrator/booking/create.html"
    form_class = BookingForm
    success_url = reverse_lazy('booking_list')
    pk_url_kwarg = 'id'

    def test_func(self):
        return self.request.user.admin or self.request.user.staff

@login_required
@user_passes_test(lambda u: u.admin or u.staff)
def delete_booking(request, id):
    booking= get_object_or_404(Booking,id=id)
    booking.delete()
    return redirect('booking_list')

class ContactUsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Contact
    template_name = "administrator/contactus/list.html"
    queryset = Contact.objects.all()

    def test_func(self):
        return self.request.user.admin

@login_required
@user_passes_test(lambda u: u.admin)
def contactus_delete(request, id):
    contactus= get_object_or_404(Contact,id=id)
    contactus.delete()
    return redirect('contact_list')

class ClassRoomListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ClassRoom
    template_name = "administrator/classroom/list.html"

    def test_func(self):
        return self.request.user.admin

class ClassRoomCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    model = ClassRoom
    fields = '__all__'
    template_name = "administrator/classroom/create.html"
    success_url = reverse_lazy('classroom_list')
    success_message = "The classroom has been created successfully"

    def test_func(self):
        return self.request.user.admin

class ClassRoomUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = ClassRoom
    fields = '__all__'
    template_name = "administrator/classroom/create.html"
    success_url = reverse_lazy('classroom_list')
    success_message = "The classroom has been updated successfully"
    pk_url_kwarg = 'id'

    def test_func(self):
        return self.request.user.admin

class ClassRoomTeachersListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ClassRoomTeachers
    template_name = "administrator/classroomteachers/list.html"

    def get_queryset(self):
        queryset = super(ClassRoomTeachersListView, self).get_queryset()
        queryset = queryset.filter(classroom_id=self.kwargs['id'])
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(ClassRoomTeachersListView, self).get_context_data(**kwargs)
        context["classroom_id"] = self.kwargs['id']
        context["classroom"] = get_object_or_404(ClassRoom, id=self.kwargs['id'])
        return context

    def test_func(self):
        return self.request.user.admin

def add_classroom_teacher_list(request, id):
    if request.method == 'GET':
        classroom_id = id
        teachers = User.objects.filter(staff=True)
        existing_teachers = ClassRoomTeachers.objects.filter(classroom_id=classroom_id)
        for i in existing_teachers:
            teachers = teachers.exclude(id=i.teacher_id)
        context = {
            'teachers': teachers,
            'selected_classroom': ClassRoom.objects.get(id=classroom_id)
        }
        return render(request, 'administrator/classroomteachers/add.html', context)

def classroom_teacher_confirm_add(request, classroom_id, teacher_id):
    teacher = get_object_or_404(User, id=teacher_id)
    classroom = get_object_or_404(ClassRoom, id=classroom_id)

    if ClassRoomTeachers.objects.filter(classroom=classroom, teacher_id=teacher_id):
        messages.error(request, "Teacher already exists")
        return redirect('classroomteachers_list', id=classroom_id)

    classroom_teacher = ClassRoomTeachers(classroom=classroom, teacher=teacher)
    classroom_teacher.save()
    messages.success(request, 'The teacher has been added successfully')
    return redirect('classroomteachers_list', id=classroom_id)

def remove_classroom_teacher(request, id):
    classroom_teacher = get_object_or_404(ClassRoomTeachers, id=id)
    classroom_teacher.delete()
    messages.success(request, 'The teacher has been removed successfully')
    return redirect('classroomteachers_list', id=classroom_teacher.classroom_id)

class NoticeboardListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Noticeboard
    template_name = "administrator/noticeboard/list.html"
    queryset = Noticeboard.objects.all().select_related('department')

    def test_func(self):
        return self.request.user.admin or self.request.user.staff

class NoticeboardDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Noticeboard
    template_name = "administrator/noticeboard/detail.html"
    pk_url_kwarg = 'id'

    def test_func(self):
        return self.request.user.admin or self.request.user.staff

class NoticeboardCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    model = Noticeboard
    fields = '__all__'
    template_name = "administrator/noticeboard/create.html"
    success_url = reverse_lazy('noticeboard_list')
    success_message = "The notice has been created successfully."

    def test_func(self):
        return self.request.user.admin or self.request.user.staff

class NoticeboardUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Noticeboard
    fields = '__all__'
    template_name = "administrator/noticeboard/create.html"
    success_url = reverse_lazy('noticeboard_list')
    success_message = "The notice has been updated successfully."
    pk_url_kwarg = 'id'

    def test_func(self):
        return self.request.user.admin or self.request.user.staff

class NoticeboardDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Noticeboard
    template_name = "administrator/noticeboard/delete.html"
    success_url = reverse_lazy('noticeboard_list')
    success_message = "The notice has been deleted successfully."
    pk_url_kwarg = 'id'
    
    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def test_func(self):
        return self.request.user.admin or self.request.user.staff

class GrievanceListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Grievance
    template_name = "administrator/grievance/list.html"
    queryset = Grievance.objects.all().select_related('department')

    def test_func(self):
        return self.request.user.admin

class GrievanceUddateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Grievance
    form_class = GrievanceUpdateForm
    template_name = "administrator/grievance/create.html"
    success_url = reverse_lazy('grievance_list')
    success_message = "The grievance has been updated successfully."
    pk_url_kwarg = 'id'
    
    def get_context_data(self, **kwargs):
        context = super(GrievanceUddateView, self).get_context_data(**kwargs)
        context["grievance"] = get_object_or_404(Grievance, id=self.kwargs['id'])
        return context

    def test_func(self):
        return self.request.user.admin

def grievance_delete(request, id):
    grievance = get_object_or_404(Grievance, id=id)
    grievance.delete()
    messages.success(request, 'The grievance has been deleted successfully')
    return redirect('grievance_list')