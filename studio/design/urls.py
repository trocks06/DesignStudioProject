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
    path('applications/custom', views.CustomApplicationsView.as_view(), name='custom_applications'),
    path('applications/all', views.AllApplicationsView.as_view(), name='all_applications'),
    path('application/<int:pk>/edit/design/', views.design_application, name='design_application'),
    path('application/<int:pk>/edit/status/', views.status_application, name='status_application'),
    path('categories/', views.categories, name='categories'),
    path('category/create/', views.create_category, name='create_category'),
    path('category/<int:pk>/delete/', views.delete_category, name='delete_category'),
]