from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profille/delete/', views.delete_profile, name='delete_profile'),
    path('profile/edit/password', views.PasswordChange.as_view(), name='password_change'),
    path('application/create', views.create_application, name='create_application'),
    path('application/<int:pk>/', views.ApplicationDetail.as_view(), name='detail_application'),
    path('application/<int:pk>/delete/', views.delete_application, name='delete_application'),
    path('custom_applications/', views.CustomApplicationsView.as_view(), name='custom_applications'),
]