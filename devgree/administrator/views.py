from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.
@login_required
@user_passes_test(lambda u: u.admin)
def admin_home(request):
    return render(request, 'administrator/home.html')

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
@user_passes_test(lambda u: u.admin or u.staff)
def delete_student(request, id):
    student = get_object_or_404(User, id=id, student=True)
    student.delete()
    return redirect('student_list')

class StaffListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Staff
    template_name = "administrator/staff/list.html"

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
    queryset = Booking.objects.select_related('room', 'event').all()

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




class NoticeListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Notice
    template_name = "administrator/notice/list.html"
    queryset = Notice.objects.select_related('event').all()

    def test_func(self):
        return self.request.user.admin or self.request.user.staff

class NoticeCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Notice
    form_class = NoticeForm
    template_name = "administrator/notice/create.html"
    success_url = reverse_lazy('notice_list')

    def test_func(self):
        return self.request.user.admin or self.request.user.staff
   

class NoticeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Notice
    template_name = "administrator/notice/create.html"
    form_class = NoticeForm
    success_url = reverse_lazy('notice_list')
    pk_url_kwarg = 'id'

    def test_func(self):
        return self.request.user.admin or self.request.user.staff


@login_required
@user_passes_test(lambda u: u.admin or u.staff)
def delete_notice(request,id ):
    notice= get_object_or_404(Notice,id=id)
    notice.delete()
    return redirect('notice_list')
