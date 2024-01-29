from django.shortcuts import render, redirect
from .forms import LoginUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd['username'], password=cd['password'])
            if user and user.is_active:
                login(request, user)
                return redirect('events:events')
    else:
        form = LoginUserForm()
    return render(request, 'app_users/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('users:login')