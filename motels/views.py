import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
from django.template.loader import render_to_string
# from django.shortcuts import HttpResponse
from django.db import IntegrityError
from django.shortcuts import HttpResponseRedirect, render, get_object_or_404, HttpResponse
from django.http import  Http404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, RegularUserHistory, Province, District
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
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404("Người dùng này không tồn tại hoặc không còn hoạt động")
    posts = user.posts.all().order_by('-id')

    context = {
        "profile": user,
        "posts": posts
    }

    return render(request, 'motels/profile.html', context)



@login_required
def create_post_category(request):
    return render(request, 'motels/create_post_category.html')

@csrf_exempt
def create_post_new(request):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('create_post_category'))

    if request.method == 'POST':
        title = request.POST["title"]
        provinces = Province.objects.all()
        try:
            category = int(request.POST["category"])
        except:
            raise Http404('Bạn gửi sai loại bài đăng rồi')

        return render(request, 'motels/create_post_new.html', {'title': title, 'category': category, 'provinces': provinces})

# API function
        
@csrf_exempt
@login_required
def edit_profile(request):
    data = dict()
    provinces = Province.objects.all()
    if request.method == 'GET':
        data['last_name'] =  request.user.last_name
        data['first_name'] = request.user.first_name
        data['user_address'] = request.user.address.id
        # data['y_address'] = serializers.serialize('json', provinces)
        data['all_address'] = [province.serialize() for province in provinces]
        return JsonResponse(data)
        
@csrf_exempt
@login_required
def save_profile(request):
    data = dict()
    user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        # Validate nếu tỉnh không có trong db
        address = request.POST.get('address')
        user.last_name = last_name
        user.first_name = first_name
        user.address = Province.objects.get(pk=address)
        user.save(force_update=True)
        data['status'] = True
        data['last_name'] =  last_name
        data['first_name'] = first_name
        return JsonResponse(data)

def get_district(request, province_id):
    data = dict()
    districts = District.objects.select_related('province').filter(province=province_id)
    data['districts'] = serializers.serialize('json', districts)
    return JsonResponse(serializers.serialize('json', districts), safe=False)
