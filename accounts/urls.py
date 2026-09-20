from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.account_list, name='accounts'),
    path('new/', views.account_create, name='create'),
    path('<int:pk>/edit/', views.account_edit, name='edit'),
    path('<int:pk>/password/', views.password_reset, name='password'),
    path('<int:pk>/delete/', views.account_delete, name='delete'),
]
