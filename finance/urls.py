from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_form, name="view_form"),
    path('your_finance/', views.your_finance, name="your_finance"),
    # Api
    path('api/callback', views.callback, name="callback"),
]