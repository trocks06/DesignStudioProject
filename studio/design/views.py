from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView

from .forms import UserLoginForm, UserRegisterForm, UserEditForm, ApplicationCreateForm, ApplicationEditForm
from .models import Application

def is_employer(user):
    return user.is_employer

def is_superuser(user):
    return user.is_superuser

def is_user(user):
    return not is_employer(user) and not is_superuser(user)

def is_employer_or_superuser(user):
    return is_employer(user) or is_superuser(user)

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
@method_decorator(user_passes_test(is_user), name='dispatch')
def create_application(request):
    if request.method == 'POST':
        form = ApplicationCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.app_publisher = request.user
            application.save()
            return redirect('index')
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

@login_required
def delete_application(request, pk):
    app = get_object_or_404(Application, pk=pk)
    user = request.user.username
    if user != app.app_publisher.username:
        messages.error(request, 'Нельзя удалить чужую заявку.')
        return redirect('detail_application', pk)
    if app.status in ['a', 'd']:
        messages.error(request, 'Нельзя удалить заявку с текущим статусом.')
        return redirect('detail_application', pk)
    if request.method == 'POST':
        app.delete()
        return redirect('index')
    else:
        return render(request, 'design/delete_application.html', {'app': app})

@method_decorator(user_passes_test(is_user), name='dispatch')
class CustomApplicationsView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'design/custom_applications.html'
    context_object_name = 'applications_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.GET.get('status')
        if status_filter:
            return queryset.filter(app_publisher=self.request.user, status=status_filter).order_by('-app_date_created')
        else:
            return queryset.filter(app_publisher=self.request.user).order_by('-app_date_created')


@method_decorator(user_passes_test(is_employer_or_superuser), name='dispatch')
class AllApplicationsView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'design/all_applications.html'
    context_object_name = 'applications_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.GET.get('status')
        if status_filter:
            return queryset.filter(status=status_filter).order_by('-app_date_created')
        else:
            return queryset.all().order_by('-app_date_created')

@login_required
@user_passes_test(is_employer)
def design_application(request, pk):
    application = get_object_or_404(Application, pk=pk)
    if request.method == 'POST':
        form = ApplicationEditForm(data=request.POST, files=request.FILES, instance=application)
        if form.is_valid():
            application = form.save(commit=False)
            application.design_publisher = request.user
            application.save()
            return redirect('detail_application', pk)
    else:
        form = ApplicationEditForm()
    context = {'form': form}
    return render(request, 'design/design_application.html', context)