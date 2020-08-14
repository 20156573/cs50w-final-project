from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.index, name="index"),
    path('register', views.register, name="register"),
    path('admin_login', LoginView.as_view(), name='admin_login'),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('<str:user_name>', views.profile, name="profile"),
    path('create_post/category', views.create_post_category, name='create_post_category'),
    path('create_post/new', views.create_post_new, name='create_post_new'),
    path('create_post/new/action', views.create_post_new_action, name='create_post_new_action'),
    path('<str:user_name>/posts/<str:title>', views.view_own_post, name='view_own_post'),
    path('<str:user_name>/saved', views.post_saved, name='post_saved'),
    
    # API route
    path('api/edit_profile', views.edit_profile, name="edit_profile"),
    path('api/save_profile', views.save_profile, name='save_profile'),
    path('api/get_district/<str:province_id>', views.get_district, name='get_district'),
    path('api/get_commune/<str:district_id>', views.get_commune, name='get_commune'),
    path('api/get_index', views.get_index, name='get_index'),
    path('api/follow', views.follow, name="follow"),
    # socket route
    path('demo/socket', views.socket, name='socket'),
]