from email.mime import image
from django.db import models
from accounts.models import User

# Create your models here.
class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField()
    description = models.CharField(max_length = 250, blank=True, null=True)
    
    def __str__(self):
        return self.name


class Course(models.Model):
    LEVELS = (
        ('UG', 'UG'),
        ('PG', 'PG'),
    )
    SEMESTERS = (
        (6, '6'),
        (8, '8'),
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    department = models.ForeignKey(to=Department,on_delete=models.CASCADE)
    level = models.CharField(max_length=25, choices=LEVELS)
    semesters = models.SmallIntegerField(choices=SEMESTERS)
    
    def __str__(self):
        return self.name

class Student(models.Model):
    BLOOD_GROUPS = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    )
    SEMESTERS = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
    )

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='student_user')
    phone = models.CharField(max_length=15, blank=True, null=True)
    course = models.ForeignKey(to=Course,on_delete=models.CASCADE)
    address = models.CharField(max_length=250, blank=True, null=True)
    blood_group = models.CharField(max_length=10, choices=BLOOD_GROUPS, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    register_number = models.CharField(max_length=20, unique=True)
    roll_number = models.CharField(max_length=20, unique=True)
    semester = models.IntegerField(choices=SEMESTERS)
    image = models.ImageField(upload_to='student_images', blank=True, null=True)

class Staff(models.Model):
    BLOOD_GROUPS = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    )
    SEMESTERS = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
    )

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='staff_user')
    phone = models.CharField(max_length=15, blank=True, null=True)
    teacher_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(to=Department,on_delete=models.CASCADE)
    address = models.CharField(max_length=250, blank=True, null=True)
    blood_group = models.CharField(max_length=10, choices=BLOOD_GROUPS, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
   

class Room(models.Model):
    FLOOR = (
        (1, '1'),
        (2, '2')
    )
    
    TYPE = (
        ('AC', 'AC'),
        ('NON AC', 'NON AC')
    )

    STATUS = (
        ('AVAILABLE', 'AVAILABLE'),
        ('UNAVAILABLE', 'UNAVAILABLE')
    )

    BLOCK = (
        ('AIDED', 'AIDED'),
        ('SELF', 'SELF')
    )

    id = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=30, blank=True, null=True, unique=True)
    room_no = models.CharField(max_length=15, blank=True, null=True, unique=True)
    capacity = models.CharField(max_length=15, unique=True)
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    status = models.CharField(max_length=25, choices=STATUS, blank=True, null=True)
    floor = models.IntegerField(blank=True, choices=FLOOR)
    block = models.CharField(max_length=10, choices=BLOCK, blank=True, null=True)
    image = models.ImageField(upload_to='room_images', blank=True, null=True)

    def __str__(self):
        return self.room_name

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    department = models.ForeignKey(to=Department,on_delete=models.CASCADE)
    description = models.CharField(max_length = 250, blank=True, null=True)
    
    def __str__(self):
        return self.name


class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    room = models.ForeignKey(to=Room,on_delete=models.CASCADE)
    booked_on = models.DateField(blank=True, null=True)
    booked_from = models.DateField(blank=True, null=True)
    booked_to = models.DateField(blank=True, null=True)
    event = models.ForeignKey(to=Event,on_delete=models.CASCADE)
    remarks = models.CharField(max_length = 250, blank=True, null=True)

class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=15, unique=True)
    message = models.CharField(max_length = 250)

class ClassRoom(models.Model):
    SEMESTERS = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    semester = models.IntegerField(choices=SEMESTERS)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    image = models.ImageField(upload_to='classroom_images', blank=True, null=True)

class ClassRoomTeachers(models.Model):
    id = models.AutoField(primary_key=True)
    classroom = models.ForeignKey(to=ClassRoom, on_delete=models.CASCADE)
    teacher = models.ForeignKey(to=User, limit_choices_to={'staff': True}, on_delete=models.CASCADE)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

class Noticeboard(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, unique=True)
    body = models.TextField()
    department = models.ForeignKey(to=Department,on_delete=models.CASCADE, blank=True, null=True)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)