from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('admin_login', LoginView.as_view(), name='admin_login'),
]