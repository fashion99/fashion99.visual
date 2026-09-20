from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='list'),
    path('new/', views.product_create, name='create'),
    path('<int:pk>/edit/', views.product_edit, name='edit'),
    path('<int:pk>/stock/', views.stock_adjust, name='stock'),
    path('<int:pk>/delete/', views.product_delete, name='delete'),
]
