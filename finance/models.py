from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
# Create your models here.
import motels
from motels.models import User, Post

from motels import util

class CardType(models.Model):
    code = models.CharField(max_length=20, verbose_name='Code')
    name = models.CharField(max_length=20, verbose_name='Telecom')
    class Meta:
        verbose_name = 'Telecom'
        verbose_name_plural = 'Telecom'

    def __str__(self):
        return self.name

class CardAmount(models.Model):
    amount = models.IntegerField(validators=[MinValueValidator(10000)], verbose_name='Amount')
    # class Meta:
    #     verbose_name = 'Mệnh giá'
    #     verbose_name_plural = 'Mệnh giá'

    def __str__(self):
        return str(self.amount)


class CardHistory(models.Model):
    status = models.IntegerField(default=99)
    message = models.CharField(max_length=50)
    request_id = models.CharField(max_length=69, verbose_name='Request id')
    value = models.IntegerField(null=True, verbose_name='Value')
    amount = models.IntegerField(null=True, verbose_name='Return Value')

    code = models.CharField(max_length=50)
    serial = models.CharField(max_length=50)
    trans_id = models.CharField(null=True, max_length=100, blank=True)
    callback_sign = models.CharField(max_length=200, blank=True)
    timestamp = models.DateTimeField(verbose_name='Time', auto_now_add=True)
    declared_value = models.ForeignKey(CardAmount, verbose_name='Declared value ', related_name='price', on_delete=models.CASCADE)
    telco = models.ForeignKey(CardType, verbose_name='Telecom', related_name='type', on_delete=models.CASCADE)
    user = models.ForeignKey(motels.models.User, related_name='cards', verbose_name='User', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'History'
        verbose_name_plural = 'History'

    def __str__(self):
        return f"{self.request_id} - {self.value} - {self.telco}"

    def get_date(self):
        return util.get_date(self, self.timestamp)

    def is_waiting(self):
        if self.status == 99:
            return True
        return False

    def is_success(self):
        if self.status == 1 or self.status == 2:
            return True
        return False
        
    def is_fail(self):
        if self.status == 3:
            return True
        return False

    def get_status(self):
        if self.status == 99:
            return 'Chờ xử lý'
        if self.status == 1 or self.status == 2:
            return 'Thành công'
        if self.status == 3:
            return 'Thất bại'

    get_date.short_description = 'Time'

class Vip(models.Model):
    amount = models.IntegerField(validators=[MinValueValidator(1000)], unique=True, verbose_name='Amount/day',  help_text='<span style="position:absolute;left:205px; top:17px ">VND</span>')
    timestamp = models.DateTimeField(verbose_name='Thời gian tạo', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Vip'
        verbose_name_plural = 'Vip'
    def __str__(self):
        return f'{self.amount}/day'
    
class Discount(models.Model):
    timestamp = models.DateTimeField(verbose_name='Thời gian tạo', auto_now_add=True)
    percent = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    day = models.IntegerField(verbose_name='Số ngày', validators=[MinValueValidator(1)])
    amount= models.ManyToManyField(Vip, blank=True, through='VipDiscount')

    class Meta:
        verbose_name = 'Discount'
        verbose_name_plural = 'Discount'

class VipDiscount(models.Model):
    vip = models.ForeignKey(Vip, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE) 
    is_active = models.BooleanField(verbose_name='Hiệu lực')

class PostedAds(models.Model):
    timestamp = models.DateTimeField(verbose_name='Thời gian đẩy', auto_now_add=True)
    days = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)], verbose_name='Số ngày chạy')
    vip_discount = models.ForeignKey(VipDiscount, verbose_name='Mã giảm giá', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, related_name='ads', verbose_name='Bài đăng', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Ads'
        verbose_name_plural = 'Ads'

    def get_how_long(self):
        return util.get_how_long(self, self.timestamp)