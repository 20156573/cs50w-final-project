import json, random, hashlib, urllib.parse, requests, pycurl, certifi
from io import StringIO 
from django.utils import timezone
from django.urls import reverse
# from cStringIO import StringIO

from django.http import JsonResponse, Http404
from django.db.models import Q, Sum
from django.shortcuts import render
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponseRedirect, HttpResponse, redirect
from .forms import RechargeForm
from .models import CardType, CardAmount, CardHistory
from django.contrib.messages import constants as message_constants
from django.contrib import messages

# Create your views here.


@login_required
def view_form(request):
    his = CardHistory.objects.select_related('user').filter(user=request.user).order_by('-id')
    finance = CardHistory.objects.select_related('user').filter(user=request.user).filter(Q(status=1)|Q(status=2)).aggregate(Sum('value'))
    if request.method == 'GET':     
        form = RechargeForm()

    if request.method == 'POST':
        form = RechargeForm(request.POST)
        if form.is_valid():
            request_id = random.randrange(100004, 99999999)
            request_id = str(request_id)
            command = 'charging'
            url = "https://thesieure.com/chargingws/v2"
            partner_id = '7833818951'
            partner_key = 'f823c010fc2e43f442a82257bb5a023d'

            code = request.POST['code'].strip()
            serial = request.POST['serial'].strip()
            declared_value = int(request.POST['declared_value'])
            telco = int(request.POST['telco'])

            if not code or not serial:
                return HttpResponse('Code và serial không được bỏ trống')
                
            try:
                telco_value = CardType.objects.get(pk=request.POST['telco']).code 
            except IntegrityError: 
                raise Http404("Loại nhà mạng này không tồn tại")

            try:
                declared_value_value = str(CardAmount.objects.get(pk=request.POST['declared_value']).amount)
            except IntegrityError: 
                raise Http404("Mệnh giá này không tồn tại")
                
            string = partner_key + code + command + partner_id + request_id + serial + telco_value
            sign = hashlib.md5(string.encode()).hexdigest()

            dataPost = dict()
            dataPost['request_id'] = request_id
            dataPost['code'] = code
            dataPost['partner_id'] = partner_id
            dataPost['serial'] = serial
            dataPost['telco'] = telco_value
            dataPost['command'] = command
            dataPost['amount'] = declared_value_value
            dataPost['sign'] = sign
            # data = urllib.parse.urlencode(dataPost)
            
            data = json.dumps(dataPost)

            len_data = len(data)
            data = StringIO(data)
            ch = pycurl.Curl()
            
            ch.setopt(pycurl.CAINFO, certifi.where())
            ch.setopt(pycurl.URL, url)
            ch.setopt(pycurl.HTTPHEADER, ['Accept: application/json',
                                'Content-Type: application/json'])
            ch.setopt(pycurl.POST, 1)
            ch.setopt(pycurl.READDATA, data)
            ch.setopt(pycurl.POSTFIELDSIZE, len_data)
            ch.perform()

            status_code = ch.getinfo(pycurl.RESPONSE_CODE)
            if status_code != 200:
                print('Aww Snap :( Server returned HTTP status code {}'.format(status_code))
            ch.close()

            callbackstring = partner_key + code + serial
            callback_sign = hashlib.md5(callbackstring.encode()).hexdigest()
            his = CardHistory(message='Thẻ chờ xử lý', request_id=request_id, value=None, amount=None, code=code, serial=serial, \
                trans_id=None, callback_sign=callback_sign, declared_value=CardAmount.objects.get(pk=declared_value), telco=CardType.objects.get(pk=telco), user=request.user)
            his.save()

            messages.add_message(
                request, messages.SUCCESS, 'Thẻ đang chờ xử lý',
                fail_silently=True,
            )
            return HttpResponseRedirect(reverse("view_form"))
    context = { 
        'form': form, 
        'finance': finance['value__sum'] or 0,
        'his': his 
        }
    return render(request, 'finance/view_form.html', context)

@csrf_exempt
def callback(request):
    if request.method == 'POST': 
        data = json.loads(request.body)

        code = data.get('code')
        serial = data.get('serial')
        partner_key = 'f823c010fc2e43f442a82257bb5a023d'

        telco = CardType.objects.filter(code=data.get('telco')).first()
        try:
            his = CardHistory.objects.filter(code=code).filter(serial=serial).filter(telco=telco).first()
            if his.callback_sign == data.get('callback_sign'):
                his.request_id = data.get('request_id')
                his.message = data.get('message')
                his.status = int(data.get('status'))
                his.value = int(data.get('value'))
                his.amount = int(data.get('amount'))
                his.trans_id = data.get('trans_id')
                his.callback_sign = data.get('callback_sign')
                his.timestamp = timezone.now()
                his.save()
            else:
                return HttpResponse('sai hash')
        except IntegrityError:
            raise Http404('Bản ghi không tồn tại')
        return HttpResponse(serial)
    return HttpResponse('ghcvhgd')

@login_required
def your_finance(request):
    
    u = request.user
    finance = CardHistory.objects.select_related('user').filter(user=u).filter(Q(status=1)|Q(status=2)).aggregate(Sum('value'))
    his = CardHistory.objects.select_related('user').filter(user=request.user).order_by('-id')
    context = {
        'his': his,
        'finance': finance['value__sum'] or 0
    }
    return render(request, 'finance/your_finance.html', context)