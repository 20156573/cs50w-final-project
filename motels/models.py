import re
from django.utils import timezone
from django.db import models
from django.utils.html import format_html
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.db.models import Value
from django.db.models.functions import Concat
from django.db import connection
from . import util
from django.utils.translation import gettext_lazy as _
# from PIL import Image
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, last_name, first_name, password=None):

        if not email:
            raise ValueError('Vui lòng nhập địa chỉ email.')
        if not password:
            raise ValueError('Vui lòng nhập password.')
        if not first_name:
            raise ValueError('Vui lòng nhập tên.')
        if not last_name:
            raise ValueError('Vui lòng nhập họ.')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, last_name, first_name, password=None):

        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name

        )
        user.is_superuser = True
        user.save(using=self._db)
        return user

# Tỉnh
class Province(models.Model): 
    id = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=100)
    type_pro = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.name}"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

class User(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(verbose_name='Email', max_length=255, unique=True)
    first_name = models.CharField(verbose_name='First name', max_length=30, null=True)
    last_name = models.CharField(verbose_name='Last name', max_length=30, null=True)
    address = models.ForeignKey(Province, on_delete=models.PROTECT, related_name='user_address', verbose_name='Địa chỉ', null=True, blank=True)
    contact_number = models.CharField(verbose_name='Phone number', max_length=12, blank=True, unique=True, null=True)
    avatar = models.ImageField( verbose_name='Avatar',upload_to='avatars/', blank=True, null=True, default='avatars/default.png')
    date_joined = models.DateField(verbose_name='Date join', auto_now_add=True)
    is_active = models.BooleanField(verbose_name='Active', default=True)
    is_superuser = models.BooleanField(verbose_name='Superuser', default=False) 
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    # class Meta:
    #     verbose_name = 'User'
    #     verbose_name_plural = 'Người dùng'

    def get_finance(self):
        with connection.cursor() as cursor:
            cursor.execute("select sum(h.value) as finance from motels_user as u join finance_cardhistory \
                as h on u.id = h.user_id and u.id = %s where h.status = %s or h.status = %s", [self.id, 1, 2])
            row = cursor.fetchone()
        
        return row[0] or 0


    def get_email_field_name(self):
        return self.email

    def get_full_name(self):
        full_name = '%s %s' % (self.last_name, self.first_name)
        if full_name == 'None None':
            return self.email
        return full_name.strip()

    def get_full_name_link(self):
        e = self.email[0:self.email.index("@")] + '.' + str(self.id)
        return e

    def __str__(self):
        return '{} <{}>'.format(self.get_full_name(), self.email)

    def get_date_joined(self):
        return '{}'.format(self.date_joined)

    def get_contact_number(self):
        if self.contact_number:
            return self.contact_number
        return ''

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
        
    # admin

    def get_login(self):
        return util.get_how_long(self, self.last_login)

    def full_name(self):
        return self.last_name  + ' ' + self.first_name
    full_name.admin_order_field = Concat('first_name', Value(' '), 'last_name')
    full_name.short_description = 'Họ tên'

# Quận
class District(models.Model):
    id = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=100)
    type_dis = models.CharField(max_length=30)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='districts')

    class Meta:
        verbose_name = 'Quận'
        verbose_name_plural = 'Quận'

    def __str__(self):
        return f"{self.name}, {self.province}"

# Huyện
class Commune(models.Model):
    id = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=100)
    type_com = models.CharField(max_length=30)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='commune')

    def __str__(self):
        return f"{self.name}, {self.district}"

# class RentersGenterChoice(models.IntegerChoices):
#     NU = 0, 'Chỉ nữ'
#     NAM = 1, 'Chỉ nam'
#     ALL = 2, 'Tất cả'

# class CategoryChoice(models.IntegerChoices):
#     ROOMATE = 0, 'Tìm bạn ở ghép'
#     ROOM = 1, 'Cho thuê phòng trọ'
#     HOUSE = 2, 'Cho thuê nhà nguyên căn'
#     APARTMENT = 3, 'Cho thuê nguyên căn chung cư'
    
class Post(models.Model):
    NU = 0
    NAM = 1
    ALL = 2

    RentersGenterChoice = [
        (NU, 'Chỉ nữ'),
        (NAM, 'Chỉ nam'),
        (ALL, 'Tất cả'),
    ]

    ROOMATE = 0
    ROOM = 1
    HOUSE = 2
    APARTMENT = 3

    CategoryChoice = [
        (ROOMATE, 'Tìm bạn ở ghép'),
        (ROOM, 'Cho thuê phòng trọ'),
        (HOUSE, 'Cho thuê nhà nguyên căn'),
        (APARTMENT, 'Cho thuê nguyên căn chung cư')
    ]

    title = models.CharField(verbose_name='Title', max_length=110)
    description = models.TextField(max_length=1000)
    area = models.FloatField(help_text='<span style="position:absolute;left:205px; top:17px ">m2</span>')
    renters_gender = models.IntegerField(verbose_name='Looking for', choices=RentersGenterChoice)
    furniture = models.TextField(max_length=500, null=True, blank=True) #nội thất

    rent = models.IntegerField(verbose_name='Ren/month',  help_text='<span style="position:absolute;left:205px; top:17px ">VND</span>') #giá thuê nhà một tháng
    deposit = models.IntegerField(null=True, blank=True,  help_text='<span style="position:absolute;left:205px; top:17px ">VND</span>') #tiền đặt cọc
    category = models.IntegerField(choices=CategoryChoice) 
    update_time = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(verbose_name='Status', default=1)

    # status 1: đang chờ duyệt
    # status 2: đã duyệt
    # status 3: đã ẩn

    #tìm người ở ghép 0
    #tìm người thuê nguyên phòng trọ 1
    #tìm người thuê nguyên căn nhà 2
    #tìm người thuê nguyên chung cư 3
    
    other_contact_info = models.CharField(verbose_name='Other contact info', max_length=35, null=True, blank=True)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    # class Meta:
    #     verbose_name = 'Tin'
    #     verbose_name_plural = 'Tin'

    def __str__(self):
        return ('User ' + str(self.poster.id) + ' - ' + self.poster.get_full_name()+ ' - ' + self.title).strip()

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "area": self.area,
            "renters_gender": self.renters_gender,
            "furniture": self.furniture,

            "rent": self.rent,
            "deposit": self.deposit,
            'update_time': self.update_time,
            'category': self.category,

            "contact_info": self.other_contact_info,
            "poster": self.poster.id,
        }
        
    def getCategory(self):
        category_c = {
            4: 'Tìm người ở ghép',
            1: 'Cho thuê phòng trọ',
            2: 'Cho thuê nhà nguyên căn',
            3: 'Cho thuê nguyên căn chung cư'
        }
        return category_c[self.category]
    getCategory.short_description = 'Category'


    def getGenderRenter(self):
        gender = {
            0: 'Nữ thuê',
            1: 'Nam thuê',
            2: 'Nam và nữ thuê'
        }
        return gender[self.renters_gender]
    

    def getUpdateTime(self):
        return util.get_how_long(self, self.update_time)

    def get_title_link(self):
        s = util.no_accent_vietnamese(self.title).replace(' ', '-').lower() + '.' + str(self.id) 
        s = s.replace("/", "---")
        return s

    def get_active(self):
        if self.status == 2 or  self.status == 7:
            return True
        return False
class PostAddress(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, primary_key=True)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, related_name='address')
    detailed_address = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.detailed_address}, {self.commune}"

class Apartment(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, primary_key=True)
    number_of_bedrooms = models.IntegerField(verbose_name='Number of bedrooms')
    number_of_toilets = models.IntegerField(verbose_name='Number of toilets')

    class Meta:
        verbose_name = 'Category: Apartment'
        # verbose_name_plural = 'Loại tin: cho thuê căn chung cư'

    def __str__(self):
        return ""

class House(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, primary_key=True)
    number_of_bedrooms = models.IntegerField(verbose_name='Number of bedrooms')
    number_of_toilets = models.IntegerField(verbose_name='Number of toilets')
    total_floor = models.IntegerField(verbose_name='Total floor')

    class Meta:
        verbose_name = 'Category: House'
        # verbose_name_plural = 'Loại tin: cho thuê nhà nguyên căn'

    def __str__(self):
        return "" 

class Room(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, primary_key=True)
    max_rent = models.IntegerField(verbose_name='Max rent', null=True, blank=True,  help_text='<span style="position:absolute;left:205px; top:17px ">VND</span>')
    number_of_rooms = models.IntegerField(verbose_name='Number of Rooms', null=True, blank=True,  help_text='<span style="position:absolute;left:205px; top:17px ">room</span>') #Số phòng trọ còn trống để cho thuê
    
    class Meta:
        verbose_name = 'Category: Room'

    def __str__(self):
        return ""

class Roommate(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, primary_key=True)
    number_of_roommate = models.IntegerField(verbose_name='Looking for', help_text='<span style="position:absolute;left:205px; top:17px ">people</span>')

    class Meta:
        verbose_name = 'Category: Roommate'
        
    def __str__(self):
        return "Thông tin chi tiết"
    

# class PostStatusChoice(models.IntegerChoices):
#     CHODUYET = 1, 'Tin của bạn đang chờ duyệt'
#     DUYET = 2, 'Tin của bạn đã được duyệt thành công'
#     KHONGDUYET = 3, 'Tin của bạn không được duyệt'
#     HUYDYCDUYET = 4, 'Bạn đã hủy yêu cầu duyệt tin'
#     ADMINAN = 5, 'Tin của bạn đã bị khóa'
#     BANAN = 6, 'Bạn đã ẩn tin của mình'
#     BOAN = 7, 'Tin đã bỏ ẩn'

class RegularUserHistory(models.Model):

    CHODUYET = 1
    DUYET = 2
    KHONGDUYET = 3
    HUYDYCDUYET = 4
    ADMINAN = 5
    BANAN = 6
    BOAN = 7

    PostStatusChoice = [
        (CHODUYET , 'Tin của bạn đang chờ duyệt'),
        (DUYET , 'Tin của bạn đã được duyệt thành công'),
        (KHONGDUYET , 'Tin của bạn không được duyệt'),
        (HUYDYCDUYET , 'Bạn đã hủy yêu cầu duyệt tin'),
        (ADMINAN , 'Tin của bạn đã bị khóa'),
        (BANAN , 'Bạn đã ẩn tin của mình'),
        (BOAN , 'Tin đã bỏ ẩn')
    ]

    created_at = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(verbose_name='Trạng thái', choices=PostStatusChoice)
    post = models.ForeignKey(Post, related_name='history', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, related_name='who', on_delete=models.PROTECT)
    class Meta:
        verbose_name = 'Tin chờ duyệt'
        verbose_name_plural = 'Tin chờ duyệt'

    def __str__(self):
        return f"{self.created_at}, {self.status}, {self.post}, {self.updated_by}"
    def get_status(self):
        if self.status == 1:
            return 'Tin của bạn đang chờ duyệt' 
        if self.status ==2:
            return 'Tin của bạn đã được duyệt thành công'
        if self.status == 3:
            return 'Tin của bạn không được duyệt'
        if self.status == 4:
            return 'Bạn đã hủy yêu cầu duyệt tin'
        if self.status == 5:
            return 'Tin của bạn đã bị khóa'
        if self.status == 6:
            return 'Bạn đã ẩn tin của mình'
        if self.status == 7:
            return 'Tin đã bỏ ẩn'
    def get_weekday(self):
        return lambda x: "Thứ hai" if x == 0 else "Thứ ba" if x == 1 else "Thứ tư"\
        if x == 2 else "Thứ năm" if x == 3 else "Thứ sáu" if x == 4 else "Thứ bảy"\
            if x == 5 else "Chủ nhật" if x == 6 else "Ngày sao hỏa"

    def get_how_many_day_ago(self):
        now = timezone.now()
        before = self.created_at
        day_left = (now.date() - before.date()).days
        week_day = self.get_weekday()(before.weekday())
        dayandmonth = f"{before.day} tháng {before.month}"
        if day_left == 0:
            return f"Hôm nay, {week_day}, {dayandmonth}"
        if day_left == 1:
            return f"Hôm qua, {week_day}, {dayandmonth}"
        if day_left == 2:
            return f"Hôm kia, {week_day}, {dayandmonth}" 
        if day_left > 2:
            return f"{day_left} ngày trước, {week_day}, {dayandmonth}"

    def get_how_long(self):
        return util.get_how_long(self, self.created_at)
    
    def get_day_left(self):
        now = timezone.now()
        before = self.created_at
        delta = now - before
        return 30 - delta.days
        

    def get_hourandminute(self):
        hour = self.created_at.hour
        if hour >= 12:
            return f"{hour}:{self.created_at.minute} PM"
        if hour < 12:
            return f"{hour}:{self.created_at.minute} AM"

class Feedback(models.Model):
    action_flag = models.IntegerField(default=3)
    feedback = models.CharField(max_length=100)

class UserFeedback(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name='reason')
    post = models.ForeignKey(Post, on_delete=models.PROTECT, related_name='object')

class Image(models.Model):
    image = models.ImageField(verbose_name='Thêm ảnh' ,upload_to='photo_post/')
    post = models.ForeignKey(Post, related_name='photos', on_delete=models.CASCADE)

    def __str__(self):
        return ""

class PostFollow(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(verbose_name='Active', default=True)
    post = models.ForeignKey(Post, related_name='followed', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='followers', on_delete=models.PROTECT)

    class Meta:
        unique_together = (("post", "follower"),)

    def __str__(self):
        return f"{self.timestamp}, {self.is_active}, {self.post}, {self.follower}"