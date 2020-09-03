import json
import time

from django.utils import timezone
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Q
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
from django.db import IntegrityError, transaction
from django.shortcuts import HttpResponseRedirect, render, get_object_or_404, HttpResponse, redirect
from django.http import  Http404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import PasswordChangeForm
from .models import *
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from finance.models import CardHistory, PostedAds
from django.contrib.auth.forms import PasswordChangeForm
from .forms import RegisterForm, AccountAuthenticationForm, UpdateProfileForm, MyChangeFormPasswordChild, RUserChangeForm
# Create your views here.



def index(request):
    context = {'list_following': None}
    
    if request.user.is_authenticated:
        user =  request.user
        list_following = PostFollow.objects.select_related('post__poster').select_related('follower').filter(follower=user, is_active='True')[:6]
        context = {'list_following': list_following}
    return render(request, "motels/index.html", context)

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
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
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


@login_required(login_url="/login")
def user_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, form.user)  # Important!
            messages.success(request, 'Mật khẩu của bạn đã được cập nhật thành công')
            return redirect('user_change_password')
    else:
        form = PasswordChangeForm(request.user)
    context={'form': form}
    return render(request, 'motels/change_password.html', context) 

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def profile(request, user_name):
    try:
        user_id = int(user_name[user_name.rindex(".")+1:len(user_name)])
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404("Id không tồn tại")
    except ValueError:
        raise Http404("Không nhận được user_name")
    if user.is_active == False:
        raise Http404("Người dùng đã ngưng hoạt động")
    if user_name != user.get_full_name_link():
        raise Http404("Sai phần đầu của gmail")

    posts = Post.objects.raw("select DISTINCT ON (id) p.id, p.title, p.rent, p.category, i.image, concat(motels_district.name, ', ', \
        motels_province.name ) as address , concat(u.last_name,' ', u.first_name) as full_name, u.avatar, motels_postfollow.is_active\
            from motels_post p \
            join motels_user as u on u.id = p.poster_id and u.is_active=true \
            left join motels_image as i on i.post_id = p.id join motels_postaddress as a on a.post_id = p.id \
            join motels_commune on motels_commune.id =  a.commune_id join motels_district on motels_district.id = motels_commune.district_id\
            join motels_province on motels_district.province_id = motels_province.id \
            left join motels_postfollow ON motels_postfollow.post_id = p.id and motels_postfollow.follower_id = %(u)s\
            where p.poster_id = %(user_id)s and (p.status = 2 or p.status = 7)  ORDER BY p.id desc, i.id desc", {'user_id': user_id, 'u': request.user.id}) 
    context = {
        "profile": user,
        "posts": posts
    }
    return render(request, 'motels/profile.html', context)


@login_required(login_url="/login")
def create_post_category(request):
    return render(request, 'motels/create_post_category.html')

@csrf_exempt
@login_required(login_url="/login")
def create_post_new(request):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('create_post_category'))

    if request.method == 'POST':
        title = request.POST["title"]
        provinces = Province.objects.all()
        try:
            category = int(request.POST["category"])
            if category < 1 or category > 4:
                raise Http404("Bạn gửi sai loại bài đăng rồi")
        except:
            raise Http404('Bạn gửi sai loại bài đăng rồi')

        return render(request, 'motels/create_post_new.html', {'title': title, 'category': category, 'provinces': provinces})

@transaction.atomic
@login_required(login_url="/login")
def create_post_new_action(request):
    if request.method == 'POST':
        try:
            title = str(request.POST['title']).rstrip()
            if not title:
                raise ValueError('Tiêu đề không được để trống')
        except ValueError as e:
            raise Http404(e)

        try:
            category = int(request.POST['category'])
            if category < 1 or category > 4:
                raise Http404("Bạn gửi sai loại bài đăng rồi")
        except:
            raise Http404('Bạn gửi sai loại bài đăng rồi')

        furniture = request.POST['furniture'] 

        try:
            description = str(request.POST['description']).rstrip()
            if not description:
                raise ValueError('Mô tả không được để trống')
        except ValueError as e:
            raise Http404(e)

        try:
            renters_gender = int(request.POST['renters_gender'])
        except:
            raise Http404('Giới tính sai rồi')
        try:
            area = float(request.POST['area'])
        except:
            raise Http404('Diện tích phải là float')
        # price
        try: 
            rent = int(request.POST['rent'])
        except:
            raise Http404('Tiền nhà phải là int')

        other_contact = request.POST['other_contact'] or None
        deposit = request.POST['deposit'] or None
        print (other_contact)
        # address
        # Kiểm tra commune tồn tại không
        try: 
            commune = Commune.objects.get(pk=request.POST['commune'])  
        except Commune.DoesNotExist:
            raise Http404('Địa chỉ này không tồn tại')

        try:
            detailed_address = str(request.POST['detailed_address']).rstrip()
            if not detailed_address:
                raise ValueError('Địa chỉ chi tiết')
        except ValueError as e:
            raise Http404(e)

        post = Post(title=title, furniture=furniture, description=description, renters_gender=renters_gender, \
            area=area, rent=rent, deposit=deposit, poster=request.user, category=category, other_contact_info=other_contact)

        address = PostAddress(post=post, commune=commune, detailed_address=detailed_address)

        if category == 4:
            # roommate
            post.save()
            try:
                number_of_roommate = int(request.POST['number_of_roommate'])
                if not number_of_roommate or number_of_roommate < 1:
                    raise Http404('Số bạn cùng phòng được nhỏ hơn 1')
            except:
                raise Http404('Số bạn cùng phòng phải là tự nhiên dương')

            roommate = Roommate(post=post, number_of_roommate=number_of_roommate)
            roommate.save()
            
        elif category == 1:
            # room
            post.save()
            number_of_rooms = request.POST['number_of_rooms'] or None
            # try:
                
            #     if number_of_rooms and number_of_rooms < 1:
            #         raise Http404('Số phòng không được nhỏ hơn 1')
            # except:
            #     raise Http404('số phòng phải là số tự nhiên dương')

            # try:
            max_rent = request.POST['max_rent'] or None
            #     if max_rent and max_rent < 1:
            #         raise Http404('Giá nhà không được nhỏ hơn 1')
            # except:
            #     raise Http404('Giá nhà phải là số tự nhiên dương')

            room = Room(post=post, number_of_rooms=number_of_rooms, max_rent=max_rent)
            room.save()
            
        elif category == 2:
            # house
            post.save()
            try:
                number_of_bedrooms = int(request.POST['number_of_bedrooms'])
                if not number_of_bedrooms or number_of_bedrooms < 1: 
                    raise Http404('Số phòng ngủ phải lơn hơn 0')
            except:
                raise Http404('Số phòng ngủ phải là số nguyên')

            try:
                number_of_toilets = int(request.POST['number_of_toilets'])
                if not number_of_toilets or number_of_toilets < 1:
                    raise Http404('Số nhà vệ sinh phải lơn hơn 0')
            except:
                raise Http404('Số nhà vệ sinh phải là số nguyên lớn hơn 0')
             
            try:
                total_floor = int(request.POST['total_floor'])
                if not total_floor or total_floor < 1:
                    raise Http404('Số tầng phải lơn hơn 0')
            except:
                raise Http404('Số tầng sinh phải là số nguyên lớn hơn 0')

            house = House(number_of_bedrooms=number_of_bedrooms, number_of_toilets=number_of_toilets, total_floor=total_floor, post=post)
            house.save()
            
        elif category == 3:
            # apartment
            post.is_apartment=True
            post.save()
            try:
                number_of_bedrooms = int(request.POST['number_of_bedrooms'])
                if not number_of_bedrooms or  number_of_bedrooms < 1:
                    raise Http404('Số phòng ngủ phải lơn hơn 0')
            except:
                raise Http404('Số phòng ngủ phải là số nguyên lớn hơn 0')

            try:
                number_of_toilets = int(request.POST['number_of_toilets'])
                if not number_of_toilets or  number_of_toilets < 1:
                    raise Http404('Số nhà vệ sinh phải lơn hơn 0')
            except:
                raise Http404('Số nhà vệ sinh phải là số nguyên lớn hơn 0')
            apartment = Apartment(number_of_toilets=number_of_toilets, number_of_bedrooms=number_of_bedrooms, post=post)
            apartment.save()
        else:
            return HttpResponse('Sai phân loại bài đăng')

        address.save()
        if bool(request.FILES.get('image', False)) == True:
            images = request.FILES.getlist('image')
            for i in range(len(images)):
                f = Image()
                f.post = post
                f.image = images[i]
                f.save()
                
        messages.add_message(
            request, messages.SUCCESS, 'Bài đăng đang chờ duyệt',
            fail_silently=True,
        )
        return HttpResponseRedirect(reverse('profile', args=[request.user.get_full_name_link()]))
    return HttpResponseRedirect(reverse('profile', args=[request.user.get_full_name_link()]))


def view_own_post(request, user_name, title):

    try:
        user_id = int(user_name[user_name.rindex(".")+1:len(user_name)])
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404("Người dùng này không tồn tại hoặc không còn hoạt động")
    except ValueError:
        raise Http404("Người dùng này không tồn tại hoặc không còn hoạt động")
    if user.is_active == False:
        raise Http404("Người dùng đã ngưng hoạt động")

    try:
        post_id = int(title[title.rindex(".")+1:len(title)])
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        raise Http404("Bài đăng không tồn tại hoặc đã bị gỡ")
    if post.status != 2 and post.status  != 7:
        raise Http404("Bài đăng không tồn tại hoặc đã bị khóa")
    image = post.photos.all()

    history = RegularUserHistory.objects.filter(post=post).order_by('-id')

    followers = PostFollow.objects.filter(is_active=True, post=post).count()
    adshis = PostedAds.objects.filter(post_id=post)
    dayleft = RegularUserHistory.objects.filter(post=post).filter(Q(status=1)|Q(status=8)).order_by('-id').first()
    context = {
        "post": post, "first_image": image[0], "image": image[1:len(image)], "followers":followers, "history":history, "adshis": adshis, 
        "dayleft": dayleft.get_day_left
    }

    return render(request, 'motels/view_post.html', context)

@login_required(login_url="/login")
def change_post(request, post_id):
    try:
        post = Post.objects.get(Q(status=2)|Q(status=7), pk=post_id)
        if post.poster_id != request.user.id:
            raise Http404('Bạn không có quyền sửa bài đăng này')
    except Post.DoesNotExist:
        raise Http404('Bài đăng không tồn tại hoặc đang bị vô hiệu hóa')
    return render(request, 'motels/change_post.html', {"post": post})

@login_required(login_url="/login")
def user_edit(request):
    my_user = request.user
    if request.method == 'GET':
        form = RUserChangeForm(instance=my_user)
    if request.method == 'POST':
        form = RUserChangeForm(request.POST, request.FILES or None, instance=my_user)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, 'Đã chỉnh sửa thành công',
                fail_silently=True,
            )
            return HttpResponseRedirect(reverse("user_edit"))
    context = {'form': form}
    return render(request, 'motels/user_edit.html', context)


# API function

@login_required(login_url="/login")
def post_saved(request, user_name):
    try:
        user_id = int(user_name[user_name.rindex(".")+1:len(user_name)])
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404("Id không tồn tại")
    except ValueError:
        raise Http404("Không nhận được user_name")
    if user_name != user.get_full_name_link():
        raise Http404("Sai phần đầu của gmail")

    posts = Post.objects.raw("select DISTINCT ON (id) p.id, p.title, p.rent, p.category, i.image, concat(motels_district.name, ', ', \
        motels_province.name ) as address , concat(u.last_name,' ', u.first_name) as full_name, u.avatar from motels_post p\
            join motels_user as u on u.id = p.poster_id and u.is_active=true left join motels_image as i on i.post_id = p.id join motels_postaddress \
                as a on a.post_id = p.id join motels_commune on motels_commune.id =  a.commune_id join motels_district on motels_district.id \
                    = motels_commune.district_id join motels_province on motels_district.province_id = motels_province.id\
                        join motels_postfollow  ON motels_postfollow.post_id = p.id and motels_postfollow.follower_id = %(user_id)s and \
                            motels_postfollow.is_active = true ORDER BY p.id desc, i.id desc", {'user_id': user_id})

    context = {
        "profile": user,
        "posts": posts
    }
    return render(request, 'motels/post_saved.html', context)

        

@login_required(login_url="/login")
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
@login_required(login_url="/login")
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
        if address is not None:
            user.address = Province.objects.get(pk=address)
        user.save(force_update=True)
        data['status'] = True
        data['last_name'] =  last_name
        data['first_name'] = first_name
        return JsonResponse(data)
    return HttpResponseRedirect(reverse('profile', args=[request.user.get_full_name_link()]))

def get_district(request, province_id):
    districts = District.objects.select_related('province').filter(province=province_id)
    return JsonResponse(serializers.serialize('json', districts), safe=False)

def get_commune(request, district_id):
    communes = Commune.objects.select_related('district').filter(district=district_id)
    return JsonResponse(serializers.serialize('json', communes), safe=False)

def get_index(request):
    start = int(request.GET.get("start") or 0)
    end = int(request.GET.get("end") or (start + 3))

    q = request.GET.get('q', '')

    cg = request.GET.get('cg', '') #category
    lt = request.GET.get('lt', '') #location

    gd = request.GET.get('gd', '') #gender
    mn = request.GET.get('mn', '') 

    print('ss', q, cg, lt, gd, mn)

    q_cg = ''
    q_lt = ''
    q_gd = ''
    q_mn = ''

    if cg != '':
        q_cg = ' and p.category = {cg}'.format(cg=cg)
    if lt != '':
        q_lt = " and motels_province.id =  '{lt}'".format(lt=str(lt))
    if gd != '' and gd == 0:
        q_gd = ' and p.renters_gender != 1'
    if gd != '' and gd == 1:
        q_gd = ' and p.renters_gender != 0'
    if mn != '':
        q_mn = 'order by x.rent {mn}'.format(mn=mn)
    print(gd)
    user_id = request.user.id

    posts = Post.objects.raw("select * from (select DISTINCT ON (id) p.id, p.title, p.rent, p.category, i.image, concat(motels_district.name, ', ', \
        motels_province.name ) as address , concat(u.last_name,' ', u.first_name) as full_name, u.avatar, motels_postfollow.is_active\
            from motels_post p \
            join motels_user as u on u.id = p.poster_id\
            left join motels_image as i on i.post_id = p.id join motels_postaddress as a on a.post_id = p.id \
            join motels_commune on motels_commune.id =  a.commune_id join motels_district on motels_district.id = motels_commune.district_id\
            join motels_province on motels_district.province_id = motels_province.id"  + q_lt + " \
            left join motels_postfollow ON motels_postfollow.post_id = p.id and motels_postfollow.follower_id = %(user_id)s" \
            +" where (p.status = 2 or p.status = 7) and UPPER(p.title) LIKE UPPER(%(title)s) " + q_cg + q_gd + " ORDER BY p.id desc, i.id desc\
            )as x " + q_mn + " LIMIT %(limit)s OFFSET %(start)s", {'user_id': user_id, 'title': "%" + str(q)   + "%", 'limit':  end - start + 1, 'start': start})

    data = []

    for i in range(len(posts)):
        post = {
            'post_id': posts[i].id,
            'poster_id': posts[i].poster.id,
            'post_link': posts[i].get_title_link(),
            'user_link': posts[i].poster.get_full_name_link(),
            'user_avatar': settings.MEDIA_URL + '/' + posts[i].avatar,
            'full_name': posts[i].full_name,
            'title': posts[i].title,
            'category': posts[i].getCategory(),
            'update_time': posts[i].getUpdateTime(),  
            'address': posts[i].address,
            'post_image': settings.MEDIA_URL  + posts[i].image,
            'description': posts[i].description,
            'is_active': posts[i].is_active,
            'rent': posts[i].rent
        }
        data.append(post)
    if start != 0: 
        time.sleep(1)

    return JsonResponse(data, safe=False)


def profile_get_post(request, user_id, section):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404("Id không tồn tại")
    if user.is_active == False:
        raise Http404("Người dùng đã ngưng hoạt động")

    if section == 'active':
        posts = Post.objects.raw("select DISTINCT ON (id) p.id, p.title, p.rent, p.category, p.status, p.update_time, i.image, concat(motels_district.name, ', ', \
        motels_province.name ) as address , concat(u.last_name,' ', u.first_name) as full_name, u.avatar, motels_postfollow.is_active\
            from motels_post p \
            join motels_user as u on u.id = p.poster_id and u.is_active=true \
            left join motels_image as i on i.post_id = p.id join motels_postaddress as a on a.post_id = p.id \
            join motels_commune on motels_commune.id =  a.commune_id join motels_district on motels_district.id = motels_commune.district_id\
            join motels_province on motels_district.province_id = motels_province.id \
            left join motels_postfollow ON motels_postfollow.post_id = p.id and motels_postfollow.follower_id = %(u)s\
            where p.poster_id = %(user_id)s and (p.status = 2 or p.status = 7)  ORDER BY p.id desc, i.id desc", {'user_id': user_id, 'u': request.user.id})
    if section == 'all':
        posts = Post.objects.raw("select DISTINCT ON (id) p.id, p.title, p.rent, p.status, p.update_time, p.category, i.image, concat(motels_district.name, ', ', \
        motels_province.name ) as address , concat(u.last_name,' ', u.first_name) as full_name, u.avatar, motels_postfollow.is_active\
            from motels_post p \
            join motels_user as u on u.id = p.poster_id and u.is_active=true \
            left join motels_image as i on i.post_id = p.id join motels_postaddress as a on a.post_id = p.id \
            join motels_commune on motels_commune.id =  a.commune_id join motels_district on motels_district.id = motels_commune.district_id\
            join motels_province on motels_district.province_id = motels_province.id \
            left join motels_postfollow ON motels_postfollow.post_id = p.id and motels_postfollow.follower_id = %(u)s\
            where p.poster_id = %(user_id)s ORDER BY p.id desc, i.id desc", {'user_id': user_id, 'u': request.user.id})
    if section == 'waiting':
        posts = Post.objects.raw("select DISTINCT ON (id) p.id, p.title, p.rent, p.status, p.update_time, p.category, i.image, concat(motels_district.name, ', ', \
        motels_province.name ) as address , concat(u.last_name,' ', u.first_name) as full_name, u.avatar, motels_postfollow.is_active\
            from motels_post p \
            join motels_user as u on u.id = p.poster_id and u.is_active=true \
            left join motels_image as i on i.post_id = p.id join motels_postaddress as a on a.post_id = p.id \
            join motels_commune on motels_commune.id =  a.commune_id join motels_district on motels_district.id = motels_commune.district_id\
            join motels_province on motels_district.province_id = motels_province.id \
            left join motels_postfollow ON motels_postfollow.post_id = p.id and motels_postfollow.follower_id = %(u)s\
            where p.poster_id = %(user_id)s and p.status = 1 ORDER BY p.id desc, i.id desc", {'user_id': user_id, 'u': request.user.id})
    if section == 'hidden':
        posts = Post.objects.raw("select DISTINCT ON (id) p.id, p.title, p.rent, p.status, p.update_time, p.category, i.image, concat(motels_district.name, ', ', \
        motels_province.name ) as address , concat(u.last_name,' ', u.first_name) as full_name, u.avatar, motels_postfollow.is_active\
            from motels_post p \
            join motels_user as u on u.id = p.poster_id and u.is_active=true \
            left join motels_image as i on i.post_id = p.id join motels_postaddress as a on a.post_id = p.id \
            join motels_commune on motels_commune.id =  a.commune_id join motels_district on motels_district.id = motels_commune.district_id\
            join motels_province on motels_district.province_id = motels_province.id \
            left join motels_postfollow ON motels_postfollow.post_id = p.id and motels_postfollow.follower_id = %(u)s\
            where p.poster_id = %(user_id)s and (p.status = 6 or p.status = 5 or p.status = 3) ORDER BY p.id desc, i.id desc", {'user_id': user_id, 'u': request.user.id})
    data = []
    for i in range(len(posts)):
        post = {
            'post_id': posts[i].id,
            'poster_id': posts[i].poster.id,
            'post_link': posts[i].get_title_link(),
            'user_link': posts[i].poster.get_full_name_link(),
            'user_avatar': settings.MEDIA_URL + '/' + posts[i].avatar,
            'full_name': posts[i].full_name,
            'title': posts[i].title,
            'category': posts[i].getCategory(),
            'update_time': posts[i].getUpdateTime(),  
            'address': posts[i].address,
            'post_image': settings.MEDIA_URL  + posts[i].image,
            'description': posts[i].description,
            'is_active': posts[i].is_active,
            'rent': posts[i].rent,
            'status': posts[i].status
        }
        data.append(post)
    return JsonResponse(data, safe=False)
        

@login_required(login_url="/login")
def follow(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    follower = request.user
    post = Post.objects.get(pk=data.get("post_id"))

    follow, created = PostFollow.objects.get_or_create(post=post, follower=follower)

    if not created:
        if follow.is_active == False:
            follow.is_active = True
            follow.timestamp = timezone.now()
        else:
            follow.is_active = False
        follow.save(force_update=True)

    data = {
        "is_active": follow.is_active,
        "title": follow.post.title,
        'title_link': follow.post.get_title_link(),
        'avatar': settings.MEDIA_URL + follow.post.poster.avatar.name,
        'full_name_link': follow.follower.get_full_name_link()

    }
    return JsonResponse(data, safe=False, status=201)

# Socket io