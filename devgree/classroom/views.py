from pyexpat.errors import messages
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from administrator.models import *
from administrator.forms import *
from django.contrib import messages

# Create your views here.

@login_required
def home(request, id):
    context = {
        'object_list': ClassroomMessage.objects.order_by('-created_on').filter(classroom_id=id)[:100],
        'classroom': get_object_or_404(ClassRoom, id=id),
    }
    if request.method == "GET":
        context['form'] = ClassroomMessageForm()
        return render(request, 'classroom/home.html', context)
    elif request.method == "POST":
        form = ClassroomMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.classroom_id = id
            message.save()
            messages.success(request, 'Message sent successfully.')
            return redirect('classroom_home', id=id)
        else:
            context['form'] = form
            return render(request, 'classroom/home.html', context)

def students(request, id):
    classroom = get_object_or_404(ClassRoom, id=id)
    context = {
        'object_list': Student.objects.select_related('user').filter(course_id=classroom.course_id, semester=classroom.semester),
        'classroom': classroom,
    }
    return render(request, 'classroom/students.html', context)

def teachers(request, id):
    classroom = get_object_or_404(ClassRoom, id=id)
    context = {
        'object_list': ClassRoomTeachers.objects.select_related('teacher').filter(classroom_id=id),
        'classroom': classroom,
    }
    return render(request, 'classroom/teachers.html', context)

@login_required
def pin_messages(request, id):
    if not request.user.staff:
        return HttpResponseForbidden()
    
    message = get_object_or_404(ClassroomMessage, id=id)
    if ClassRoomTeachers.objects.filter(teacher=request.user, classroom=message.classroom_id).first():
        if message.is_pinned:
            message.is_pinned = False
        else:
            message.is_pinned = True
        message.save()
        messages.success(request, 'Message pinned successfully.')
    else:
        messages.error(request, 'You are not authorized to pin this message.')
    return redirect('classroom_home', id=message.classroom_id)


@login_required
def join_classroom(request):
    context = {}
    student = Student.objects.filter(user=request.user).first()
    if student is None:
        return HttpResponseNotFound()

    classroom = ClassRoom.objects.filter(course_id = student.course_id, semester = student.semester).first()

    if classroom is None:
        context["message"] = "No classroom has been created."
        return render(request, 'join_classroom.html', context)
    
    return redirect('classroom_home', id=classroom.id)