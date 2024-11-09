from lib2to3.fixes.fix_input import context

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView

from .forms import UserLoginForm, UserRegisterForm, UserEditForm, ApplicationCreateForm
from .models import Application

class IndexView(ListView):
    template_name = 'design/index.html'
    context_object_name = 'applications_list'

    def get_queryset(self):
        return Application.objects.filter(status='d').order_by('-app_date_created')[:4]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accepted_count'] = Application.objects.filter(status='a').count()
        return context

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect('profile')
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

@login_required
def create_application(request):
    if request.method == 'POST':
        form = ApplicationCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.app_publisher = request.user
            application.save()
            return redirect('index')
        else:
            print(form.errors)
    else:
        form = ApplicationCreateForm()
    context = {'form': form}
    return render(request, 'design/create_application.html', context)

class ApplicationDetail(LoginRequiredMixin, DetailView):
    model = Application
    template_name = 'design/detail_application.html'
    context_object_name = 'application'

    def get_object(self, queryset=None):
        application = super().get_object(queryset)
        if not application:
            raise Http404('Заявка недоступна')
        return application

def delete_application(request, pk):
    app = get_object_or_404(Application, pk=pk)
    if request.method == 'POST':
        app.delete()
        return redirect('index')
    else:
        return render(request, 'design/delete_application.html', {'app': app})

class CustomApplicationsView(LoginRequiredMixin, ListView):
    template_name = 'design/custom_applications.html'
    context_object_name = 'applications_list'

    def get_queryset(self):
        return Application.objects.filter(app_publisher=self.request.user).order_by('-app_date_created')