from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout
from django.views.generic import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# Create your views here.
def user_login(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})
    elif request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.admin:
                    return redirect('/administrator')
                elif user.staff:
                    return redirect('/staff')
                else:
                    return redirect('/student')
            return render(request, 'accounts/login.html', {'form': form})
        else:
            return render(request, 'accounts/login.html', {'form': form})
    

def user_logout(request):
    logout(request)
    return redirect('/')

class UpdateProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'accounts/profile.html'
    fields = ['first_name', 'last_name', 'email']
    success_url = reverse_lazy('edit_profile')
    success_message = 'Profile updated successfully.'

    def get_object(self):
        return self.request.user

def password_update(request):
    if request.method == 'GET':
        form = PasswordChangeForm(user=request.user)
        return render(request, 'accounts/password_update.html', {'form': form})
    elif request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('edit_profile')
        else:
            return render(request, 'accounts/password_update.html', {'form': form})