from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.index, name="index"),
    path('dang_ky/', views.register, name="register"),
    path('login/', LoginView.as_view(), name='admin_login'),
    path('dang_nhap/', views.login_view, name="login"),
    path('dang_xuat/', views.logout_view, name="logout"),
    path('<int:user_id>', views.profile, name="profile"),
    
    # API route
    path('update_profile', views.update_profile, name="update_profile"),
]