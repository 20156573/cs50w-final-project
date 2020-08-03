import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
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

def profile(request, username):

    try:
        user_id = int(username[username.rindex(".")+1:len(username)])
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404("Người dùng này không tồn tại hoặc không còn hoạt động")
 
    except ValueError:
        raise Http404("Value error")
    if username != user.get_full_name_link():
        raise Http404("Người dùng này không tồn tại hoặc không còn hoạt động")

    posts = Post.objects.raw("select DISTINCT ON (id) p.id, p.title, p.rent, p.category, i.image, concat\
        (motels_district.name, ', ', motels_province.name ) as address from motels_post p \
        left join motels_image as i on i.post_id = p.id join motels_postaddress as a on a.post_id = p.id \
        join motels_commune on motels_commune.id =  a.commune_id \
        join motels_district on motels_district.id = motels_commune.district_id join motels_province on motels_district.province_id \
        = motels_province.id ORDER BY p.id desc, i.id desc")

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
            area=area, rent=rent, deposit=deposit, poster=request.user, category=category)
        address = PostAddress(post=post, commune=commune, detailed_address=detailed_address)

        if category == '0':
            # roommate
            post.save()
            number_of_roommate = request.POST['number_of_roommate']
            roommate = Roommate(post=post, number_of_roommate=number_of_roommate)
            roommate.save()
            
        elif category == '1':
            # room
            post.save()
            number_of_rooms = request.POST['number_of_rooms'] or None
            max_rent = request.POST['max_rent'] or None
            room = Room(post=post, number_of_rooms=number_of_rooms, max_rent=max_rent)
            room.save()
            
        elif category == '2':
            # house
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
        # return HttpResponse(request.FILES['image'])
        if bool(request.FILES.get('image', False)) == True:
        # if request.FILES['image']:
            images = request.FILES.getlist('image')
            for i in range(len(images)):
                f = Image()
                f.post = post
                f.image = images[i]
                f.save()
        return HttpResponseRedirect(reverse('profile', args=(request.user.id,)))
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
        if request.user.address == None:
            data['user_address'] = request.user.address
        else:
            data['user_address'] = request.user.address.id
        data['all_address'] = [province.serialize() for province in provinces]
        return JsonResponse(data)
    return HttpResponseRedirect(reverse('profile', args=(request.user.get_full_name_link(),)))
        
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
    return HttpResponseRedirect(reverse('profile', args=(request.user.get_full_name_link(),)))

def get_district(request, province_id):
    districts = District.objects.select_related('province').filter(province=province_id)
    return JsonResponse(serializers.serialize('json', districts), safe=False)

def get_commune(request, district_id):
    communes = Commune.objects.select_related('district').filter(district=district_id)
    return JsonResponse(serializers.serialize('json', communes), safe=False)

def view_own_post(request, username, title, post_id):
    try:
        user_id = int(username[username.rindex(".")+1:len(username)])
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404("Người dùng này không tồn tại hoặc không còn hoạt động")
    except ValueError:
        raise Http404("Người dùng này không tồn tại hoặc không còn hoạt động")

    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        raise Http404("Bài đăng không tồn tại hoặc đã bị gỡ")
    
    context = {
        "post": post
    }

    return render(request, 'motels/view_post.html', context)

