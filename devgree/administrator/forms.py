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


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }     

class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
        widgets = {
            'booked_on': forms.DateInput(attrs={'type': 'date'}),
            'booked_from': forms.DateInput(attrs={'type': 'date'}),
            'booked_to': forms.DateInput(attrs={'type': 'date'}),
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        room = self.cleaned_data.get('room')
        booked_on = cleaned_data.get("booked_on")
        booked_from = cleaned_data.get('booked_from')
        booked_to = cleaned_data.get('booked_to')

        bookings_from_db = Booking.objects.filter(booked_from__lte=booked_from, booked_to__gte=booked_to, room_id=room)
        if bookings_from_db.exists():
            self.add_error('booked_from', 'Booking already exists in this date range.')

        bookings_from_db = Booking.objects.filter(booked_from__lte=booked_from, booked_to__lte=booked_to, room_id=room)
        # if bookings_from_db.exists():
        #     self.add_error('booked_from', 'Booking already exists in this date range.2')

        if booked_from > booked_to:
            self.add_error('booked_from', 'Booking from date must be before booking to date.')

        if booked_on > booked_from:
            self.add_error('booked_on', 'It must be before the booking date.')
        return cleaned_data

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
        } 

class ClassRoomTeacherAddForm(ModelForm):
    class Meta:
        model = ClassRoomTeachers
        fields = '__all__'

class ClassroomMessageForm(ModelForm):
    class Meta:
        model = ClassroomMessage
        fields = ['message', 'file']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
        }

class GrievanceCreateForm(ModelForm):
    class Meta:
        model = Grievance
        fields = ['name', 'email', 'subject', 'message', 'phone', 'department', 'created_by']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
        }

class GrievanceUpdateForm(ModelForm):
    class Meta:
        model = Grievance
        fields = ['status', 'response']
        widgets = {
            'response': forms.Textarea(attrs={'rows': 3, 'class': 'w-full'}),
            'status': forms.Select(attrs={'class': 'w-full'}),
        }

class GrievanceViewForm(ModelForm):
    class Meta:
        model = Grievance
        fields = '__all__'
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
            'response': forms.Textarea(attrs={'rows': 3}),
        }