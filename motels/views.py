import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
from django.template.loader import render_to_string
# from django.shortcuts import HttpResponse
from django.db import IntegrityError, transaction
from django.shortcuts import HttpResponseRedirect, render, get_object_or_404, HttpResponse
from django.http import  Http404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import *
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

@transaction.atomic
def create_post_new_action(request):
    if request.method == 'POST':
        title = request.POST['title']
        category = request.POST['category']
        furniture = request.POST['furniture'] 
        description = request.POST['description']
        renters_gender = request.POST['renters_gender']
        area = request.POST['area']
        # price
        rent = request.POST['rent']
        deposit = request.POST['deposit'] or None
        
        # address
        # Kiểm tra commune tồn tại không
        commune = Commune.objects.get(pk=request.POST['commune'])  
        detailed_address = request.POST['detailed_address']

        post = Post(title=title, furniture=furniture, description=description, renters_gender=renters_gender, \
            area=area, rent=rent, deposit=deposit, poster=request.user)
        address = PostAddress(post=post, commune=commune, detailed_address=detailed_address)

        if category == '0':
            # roommate
            post.is_roommate=True
            post.save()
            number_of_roommate = request.POST['number_of_roommate']
            roommate = Roommate(post=post, number_of_roommate=number_of_roommate)
            roommate.save()
            
        elif category == '1':
            # room
            post.is_room=True
            post.save()
            number_of_rooms = request.POST['number_of_rooms'] or None
            max_rent = request.POST['max_rent'] or None
            room = Room(post=post, number_of_rooms=number_of_rooms, max_rent=max_rent)
            room.save()
            
        elif category == '2':
            # house
            post.is_house=True
            post.save()
            number_of_bedrooms = request.POST['number_of_bedrooms']
            number_of_toilets = request.POST['number_of_toilets']
            total_floor = request.POST['total_floor']
            house = House(number_of_bedrooms=number_of_bedrooms, number_of_toilets=number_of_toilets, total_floor=total_floor, post=post)
            house.save()
            
        elif category == '3':
            # apartment
            post.is_apartment=True
            post.save()
            number_of_bedrooms = request.POST['number_of_bedrooms']
            number_of_toilets = request.POST['number_of_toilets']
            apartment = Apartment(number_of_toilets=number_of_toilets, number_of_bedrooms=number_of_bedrooms, post=post)
            apartment.save()
        else:
            return HttpResponse('Sai phân loại bài đăng')
        address.save()
        return HttpResponseRedirect(reverse('create_post_category'))
    return HttpResponseRedirect(reverse('profile', args=(request.user.id,)))
    
# API function
        
@csrf_exempt
@login_required
def edit_profile(request):
    data = dict()
    provinces = Province.objects.all()
    if request.method == 'POST':
        data['last_name'] =  request.user.last_name
        data['first_name'] = request.user.first_name
        data['user_address'] = request.user.address.id
        # data['y_address'] = serializers.serialize('json', provinces)
        data['all_address'] = [province.serialize() for province in provinces]
        return JsonResponse(data)
    return HttpResponseRedirect(reverse('profile', args=(request.user.id,)))
        
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
    return HttpResponseRedirect(reverse('profile', args=(request.user.id,)))

def get_district(request, province_id):
    districts = District.objects.select_related('province').filter(province=province_id)
    return JsonResponse(serializers.serialize('json', districts), safe=False)

def get_commune(request, district_id):
    communes = Commune.objects.select_related('district').filter(district=district_id)
    return JsonResponse(serializers.serialize('json', communes), safe=False)

