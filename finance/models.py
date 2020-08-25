from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
import motels
from motels.models import User, Post

from motels import util

class CardType(models.Model):
    code = models.CharField(max_length=20, verbose_name='Code')
    name = models.CharField(max_length=20, verbose_name='Nhà mạng')
    class Meta:
        verbose_name = 'Nhà mạng'
        verbose_name_plural = 'Nhà mạng'

    def __str__(self):
        return self.name

class CardAmount(models.Model):
    amount = models.IntegerField(validators=[MinValueValidator(10000)], verbose_name='Mệnh giá')
    class Meta:
        verbose_name = 'Mệnh giá'
        verbose_name_plural = 'Mệnh giá'

    def __str__(self):
        return str(self.amount)


class CardHistory(models.Model):
    status = models.IntegerField(default=99)
    message = models.CharField(max_length=50, verbose_name='Ghi chú')
    request_id = models.CharField(max_length=69, verbose_name='Mã giao dịch')
    value = models.IntegerField(null=True, verbose_name='Giá trị thẻ')
    amount = models.IntegerField(null=True, verbose_name='Thu về')

    code = models.CharField(max_length=50, verbose_name='Mã thẻ')
    serial = models.CharField(max_length=50, verbose_name='Số seri')
    trans_id = models.CharField(null=True, max_length=100, blank=True)
    callback_sign = models.CharField(max_length=200, blank=True)
    timestamp = models.DateTimeField(verbose_name='Ngày nạp', auto_now_add=True)
    declared_value = models.ForeignKey(CardAmount, verbose_name='Tiền nạp', related_name='price', on_delete=models.CASCADE)
    telco = models.ForeignKey(CardType, verbose_name='Nhà mạng', related_name='type', on_delete=models.CASCADE)
    user = models.ForeignKey(motels.models.User, related_name='cards', verbose_name='Người nạp', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Lịch sử nạp'
        verbose_name_plural = 'Lịch sử nạp'

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

    get_date.short_description = 'Ngày nạp'

class Vip(models.Model):
    amount = models.IntegerField(validators=[MinValueValidator(10000)], verbose_name='Giá trị')
    timestamp = models.DateTimeField(verbose_name='Thời gian tạo', auto_now_add=True)

    class Meta:
        verbose_name = 'Các gói Vip'
        verbose_name_plural = 'Các gói Vip'
    
class Discount(models.Model):
    timestamp = models.DateTimeField(verbose_name='Thời gian tạo', auto_now_add=True)
    percent = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    day = models.IntegerField(verbose_name='Số ngày', validators=[MinValueValidator(1)])
    is_active = models.BooleanField(verbose_name='Hiệu lực')

    class Meta:
        verbose_name = 'Các gói giảm giá'
        verbose_name_plural = 'Các gói giảm giá'

class PostedAds(models.Model):
    timestamp = models.DateTimeField(verbose_name='Thời gian đẩy', auto_now_add=True)
    days = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)], verbose_name='Số ngày chạy')
    discount = models.ForeignKey(Discount, verbose_name='Mã giảm giá', on_delete=models.CASCADE, null=True)
    vip = models.ForeignKey(Vip, verbose_name='Gói vip', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='card', verbose_name='Mệnh giá', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Lịch sử đẩy tin'
        verbose_name_plural = 'Lịch sử đẩy tin'