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
    path('user/password_change/', views.user_change_password, name='user_change_password'),
    path('user/edit/', views.user_edit, name='user_edit'),
    path('<int:post_id>/change/', views.change_post, name='change_post'),
    # API route
    path('api/edit_profile', views.edit_profile, name="edit_profile"),
    path('api/save_profile', views.save_profile, name='save_profile'),
    path('api/get_district/<str:province_id>', views.get_district, name='get_district'),
    path('api/get_commune/<str:district_id>', views.get_commune, name='get_commune'),
    path('api/get_index', views.get_index, name='get_index'),
    path('api/follow', views.follow, name="follow"),
    path('<int:user_id>/post/<str:section>/', views.profile_get_post, name='profile_get_post'),
    # socket route
#     path(
#     'admin/password_reset/done/',
#     auth_views.PasswordResetDoneView.as_view(),
#     name='password_reset_done',
# ),
]