from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from administrator.models import *

# Create your views here.
def home(request):
    return render(request, 'student/home.html')

def notice(request):
    student = Student.objects.get(user=request.user)
    context={
        'object_list': Noticeboard.objects.filter(department_id=student.course.department_id)
    }
    return render(request, 'student/notice.html', context)

def notice_view(request, id):
    notice = Noticeboard.objects.get(id=id)
    context={
        'object': notice
    }
    return render(request, 'student/notice_view.html', context)