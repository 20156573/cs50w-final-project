from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('admin_login', views.admin_login, name='admin_login'),
    path('admin_index', views.admin_index, name='admin_index'),
    path('admin_user', views.admin_user, name='admin_user'),
    # api
    path('api_index/<int:num>/', views.api_index, name='api_index'),
]