from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from administrator.models import *

# Create your views here.
def home(request):
    return render(request, 'student/home.html')

def notice(request):
    
    context={
        'object_list': Noticeboard.objects.filter(department_id=user.)
    }
