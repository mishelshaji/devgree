from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout

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
            return render(request, 'accounts/login.html', {'form': form})
        else:
            return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('/')