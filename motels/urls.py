from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.index, name="index"),
    path('register', views.register, name="register"),
    path('admin_login', LoginView.as_view(), name='admin_login'),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('<int:user_id>', views.profile, name="profile"),
    path('create_post/category', views.create_post_category, name='create_post_category'),
    path('create_post/new', views.create_post_new, name='create_post_new'),
    # API route
    path('edit_profile', views.edit_profile, name="edit_profile"),
    path('save_profile', views.save_profile, name='save_profile'),
    path('get_district/<int:province_id>', views.get_district, name='get_district'),
]