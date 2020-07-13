import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
# from django.shortcuts import HttpResponse
from django.db import IntegrityError
from django.shortcuts import HttpResponseRedirect, render, get_object_or_404
from django.http import  Http404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, RegularUserHistory
from .forms import RegisterForm, AccountAuthenticationForm, UpdateProfileForm
# Create your views here.

def index(request):
    return render(request, "motels/index.html")

def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            raw_password = form.cleaned_data.get('password1')
            # confirmation = form.cleaned_data.get('password2')
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            user = authenticate(email=email, password=raw_password, first_name=first_name, last_name=last_name)
            login(request, user)    
            return HttpResponseRedirect(reverse("index"))

    elif request.method == 'GET':
        form = RegisterForm()
        
    context = {
        "form": form,
    }
    return render(request, 'motels/register.html', context)
def login_view(request):

    if request.method == 'POST':
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(email=email, password=password)
            if user and user.is_active: 
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
        
    elif request.method == 'GET':     
        form = AccountAuthenticationForm()

    context = {
        "form": form,
    }
    return render(request, 'motels/login.html', context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def profile(request, user_id):
    form_edit_profile = []
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404("Người dùng này không tồn tại hoặc không còn hoạt động")
    posts = user.posts.all().order_by('-id')
    if request.method == 'GET':
        profile = get_object_or_404(User, pk=user_id)
        form_edit_profile = UpdateProfileForm(instance=profile)

    context = {
        "profile": user,
        "posts": posts,
        "form_edit_profile": form_edit_profile
    }

    return render(request, 'motels/profile.html', context)

@csrf_exempt
@login_required
def update_profile(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    
    return JsonResponse({"message": "Sửa thông tin thành công."}, status=201)