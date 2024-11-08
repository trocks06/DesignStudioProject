from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.urls import reverse_lazy

from .forms import UserLoginForm, UserRegisterForm, UserEditForm, ApplicationCreateForm


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

@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required
def profile(request):
    user = request.user
    context = {'user': user}
    return render(request, 'design/profile.html', context)

@login_required
def delete_profile(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        logout(request)
        return redirect('index')
    else:
        context = {'user': user}
        return render(request, 'design/delete_profile.html', context)

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserEditForm(instance=user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
    else:
        form = UserEditForm(instance=user)
    context = {'form': form}
    return render(request, 'design/edit_profile.html', context)

class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    template_name = 'design/password_change.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        return super().form_valid(form)

def create_application(request):
    if request.method == 'POST':
        form = ApplicationCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            print(form.errors)
    else:
        form = ApplicationCreateForm()
    context = {'form': form}
    return render(request, 'design/create_application.html', context)