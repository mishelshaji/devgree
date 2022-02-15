from django.shortcuts import render
from administrator.forms import *
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.
def home(request):
    context = {
        'departments': Department.objects.all(),
    }
    return render(request, 'user/home.html', context)

def notice(request):
    return render(request, 'user/notice.html')

class ContactUsCreateView(SuccessMessageMixin, CreateView):
    form_class = ContactForm
    template_name = 'user/contact.html'
    success_url = reverse_lazy('contact')
    success_message = 'Your message has been sent successfully.'

class NoticeboardListView(ListView):
    model = Noticeboard
    template_name = 'user/noticeboard/list.html'
    queryset = Noticeboard.objects.filter(department__isnull=True)

class NoticeboardDetailView(DetailView):
    model = Noticeboard
    template_name = 'user/noticeboard/detail.html'
    pk_url_kwarg = 'id'