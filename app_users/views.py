from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginUserForm, FilterForm, EventForm, EndpointDirectForm, EmbededFieldsForm, EmbededFooterForm, EndpointEmbededForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from app_hooks.models import EndpointDirect


def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd['username'], password=cd['password'])
            if user and user.is_active:
                login(request, user)
                return redirect('events')
    else:
        form = LoginUserForm()
    return render(request, 'app_users/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('users:login')


def add_filter(request):
    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('events')
    else:
        form = FilterForm()

    return render(request, 'app_users/filter.html', {'form': form})


def add_endpoint(request):
    if request.method == 'POST':
        form = EndpointDirectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('events')
    else:
        form = EndpointDirectForm()
    return render(request, 'app_users/endpointdirect.html', {'form': form})


def add_embededfields(request):
    if request.method == 'POST':
        form = EmbededFieldsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('events')
    else:
        form = EmbededFieldsForm()
    return render(request, 'app_users/embededfields.html', {'form': form})


def add_embededfooter(request):
    if request.method == 'POST':
        form = EmbededFooterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('events')
    else:
        form = EmbededFooterForm()
    return render(request, 'app_users/embededfooter.html', {'form': form})


def add_endpointembeded(request):
    if request.method == 'POST':
        form = EndpointEmbededForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('events')
    else:
        form = EndpointEmbededForm()
    return render(request, 'app_users/endpointembeded.html', {'form': form})
