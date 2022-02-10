from django.shortcuts import render
from administrator.forms import *
from django.views.generic import CreateView

# Create your views here.
def home(request):
    return render(request, 'user/home.html')

def notice(request):
    return render(request, 'user/notice.html')

class ContactUsCreateView(CreateView):
    form_class = ContactForm
    template_name = 'user/contact.html'
    success_url = '/'