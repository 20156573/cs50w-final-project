from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect, render, get_object_or_404, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import AccountAuthenticationForm
from django.urls import reverse
from django.http import JsonResponse    
from django.db.models import Q, Sum
import json
from django.utils import timezone
from datetime import datetime
from finance.models import *
from motels.models import *
# Create your views here.

def admin_login(request):
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
                return HttpResponseRedirect(reverse("admin_index"))
        
    elif request.method == 'GET':     
        form = AccountAuthenticationForm()

    context = {
        "form": form,
    }
    return render(request, 'myadmin/login.html', context)

def admin_index(request):
    return render(request, 'myadmin/index.html')

def admin_user(request):
    q = request.GET.get('q', '')
    time = request.GET.get('time', '')
    is_admin = request.GET.get('is_admin', '')
    is_superuser = request.GET.get('is_superuser', '')
    # return HttpResponse((q, time, is_admin, is_superuser))
    users = User.objects.raw('select u.id, (select sum(h.value) as finance from finance_cardhistory as h where h.user_id = u.id and (h.status=1 or h.status=2)),\
        (select count (p.id) as all_post from motels_post as p where p.poster_id = u.id)\
         from motels_user as u')
    count = User.objects.count()
    context = {
        'users': users,
        'count_user': count 
    }
    return render(request, 'myadmin/user.html', context)
# API

def api_index(request, num):
    now = timezone.now()
    if num == 1:
        before = datetime(now.year, now.month, now.day, 0, 0, 0, 0)
        finance = CardHistory.objects.select_related('user').filter(timestamp__range=(before, now)).filter(Q(status=1)|Q(status=2)).aggregate(Sum('amount'))
        post = RegularUserHistory.objects.filter(status=1).filter(created_at__range=(before, now)).count() 
        user = User.objects.filter(date_joined__range=(before, now)).count()

    if num == 2:
        today = now.weekday()
        before = now -  timezone.timedelta(today)
        finance = CardHistory.objects.select_related('user').filter(timestamp__range=(before, now)).filter(Q(status=1)|Q(status=2)).aggregate(Sum('amount'))
        post = RegularUserHistory.objects.filter(status=1).filter(created_at__range=(before, now)).count()  
        user = User.objects.filter(date_joined__range=(before, now)).count()

    if num == 3:
        today = now.weekday()
        before = datetime(now.year, now.month, 1, 0, 0, 0, 0)
        finance = CardHistory.objects.select_related('user').filter(timestamp__range=(before, now)).filter(Q(status=1)|Q(status=2)).aggregate(Sum('amount'))
        post = RegularUserHistory.objects.filter(status=1).filter(created_at__range=(before, now)).count()  
        user = User.objects.filter(date_joined__range=(before, now)).count()

    if num == 4:
        today = now.weekday()
        before = datetime(now.year, 1, 1, 0, 0, 0, 0)
        finance = CardHistory.objects.select_related('user').filter(timestamp__range=(before, now)).filter(Q(status=1)|Q(status=2)).aggregate(Sum('amount'))
        post = RegularUserHistory.objects.filter(status=1).filter(created_at__range=(before, now)).count() 
        user = User.objects.filter(date_joined__range=(before, now)).count()
    
    if num == 5:
        finance = CardHistory.objects.select_related('user').filter(Q(status=1)|Q(status=2)).aggregate(Sum('amount'))
        post = RegularUserHistory.objects.filter(status=1).count() 
        user = User.objects.count()


    data = dict()
    data['finance'] = finance['amount__sum'] or 0
    data['post'] = post
    data['user'] = user
    return JsonResponse(data, safe=False, status=200)
        
