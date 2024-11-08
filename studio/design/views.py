from django.shortcuts import render, redirect
from django.contrib import auth

from .forms import UserLoginForm, UserRegisterForm


def index(request):
    return render(request, 'design/index.html')

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect('index')
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'design/login.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'design/register.html', context)

def logout(request):
    auth.logout(request)
    return redirect('login')

