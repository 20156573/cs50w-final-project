from django.utils import timezone
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
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
            last_name=last_name
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
        user.is_staff = True
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
    address = models.ForeignKey(Province, on_delete=models.PROTECT, related_name='user_address', verbose_name='Address', null=True, blank=True)
    contact_number = models.CharField(verbose_name='Contact Number', max_length=12, blank=True, unique=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, default='avatars/default.png')
    date_joined = models.DateField(verbose_name='Date joined', auto_now_add=True)
    is_active = models.BooleanField(verbose_name='Active', default=True)
    is_staff = models.BooleanField(verbose_name='Staff', default=False)
    is_superuser = models.BooleanField(verbose_name='Superuser', default=False) 
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_email_field_name(self):
        return self.email

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        if full_name == 'None None':
            return self.email
        return full_name.strip()

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

# Quận
class District(models.Model):
    id = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=100)
    type_dis = models.CharField(max_length=30)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='districts')
    
    def __str__(self):
        return f"{self.type_dis} {self.name}, {self.province}"

# Huyện
class Commune(models.Model):
    id = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=100)
    type_com = models.CharField(max_length=30)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='commune')

    def __str__(self):
        return f"{self.type_com}, {self.name}, {self.district}"


class Post(models.Model):

    title = models.CharField(max_length=110)
    description = models.TextField(max_length=1000)
    area = models.FloatField()
    renters_gender = models.IntegerField()
    furniture = models.TextField(max_length=500, null=True, blank=True) #nội thất

    rent = models.IntegerField() #giá thuê nhà một tháng
    deposit = models.IntegerField(null=True, blank=True) #tiền đặt cọc
    
    is_roommate = models.BooleanField(default=False) #tìm người ở ghép
    is_room = models.BooleanField(default=False) #tìm người thuê nguyên phòng trọ
    is_house = models.BooleanField(default=False) #tìm người thuê nguyên căn nhà
    is_apartment = models.BooleanField(default=False) #tìm người thuê nguyên chung cư
    
    other_contact_info = models.CharField(max_length=35, null=True, blank=True)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

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

            "is_roommate": self.is_roommate,
            "is_room": self.is_room,
            "is_house": self.is_house,
            "is_apartment": self.is_apartment,

            "contact_info": self.other_contact_info,
            "poster": self.poster.id,
        }

class PostAddress(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, primary_key=True)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, related_name='address')
    detailed_address = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.detailed_address}, {self.commune}"

class Apartment(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, primary_key=True)
    number_of_bedrooms = models.IntegerField()
    number_of_toilets = models.IntegerField()

    def __str__(self):
        return f"{self.post}, có {self.number_of_bedrooms} phòng ngủ, \
            có {self.number_of_toilets} phòng vệ sinh"

class House(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, primary_key=True)
    number_of_bedrooms = models.IntegerField()
    number_of_toilets = models.IntegerField()
    total_floor = models.IntegerField()

    def __str__(self):
        return f"{self.post}, nhà có {self.number_of_bedrooms} phòng ngủ, \
            có {self.number_of_toilets} phòng vệ sinh, \
                nhà có {self.total_floor} tầng"

class Room(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, primary_key=True)
    max_rent = models.IntegerField(null=True, blank=True)
    number_of_rooms = models.IntegerField(null=True, blank=True) #Số phòng trọ còn trống để cho thuê

    def __str__(self):
        return f"{self.post}, còn {self.number_of_rooms} phòng trống"

class Roommate(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, primary_key=True)
    number_of_roommate = models.IntegerField()

    def __str__(self):
        return f"{self.post}, tìm {self.number_of_roommate} người ở ghép"
    
class PostStatus(models.Model):
    status = models.CharField(verbose_name='Status', max_length=400)
    is_active = models.BooleanField(verbose_name='Active', default=False)

    def __str__(self):
        return f"{self.status}"

class RegularUserHistory(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    post_status = models.ForeignKey(PostStatus, related_name='message', on_delete=models.PROTECT, null = True)
    post = models.ForeignKey(Post, related_name='history', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, related_name='who', on_delete=models.PROTECT, null = True)

    def __str__(self):
        return f"{self.timestamp}, {self.post_status}, {self.post}, {self.updated_by}"
        
    def get_weekday(self):
        return lambda x: "Thứ hai" if x == 0 else "Thứ ba" if x == 1 else "Thứ tư"\
        if x == 2 else "Thứ năm" if x == 3 else "Thứ sáu" if x == 4 else "Thứ bảy"\
            if x == 5 else "Chủ nhật" if x == 6 else "Ngày sao hỏa"

    def get_how_many_day_ago(self):
        now = timezone.now()
        before = self.timestamp
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

    def get_hourandminute(self):
        hour = self.timestamp.hour
        if hour >= 12:
            return f"{hour}:{self.timestamp.minute} PM"
        if hour < 12:
            return f"{hour}:{self.timestamp.minute} AM"

class Feedback(models.Model):
    feedback = models.CharField(max_length=70, blank=True)

class OtherFeedback(models.Model):
    feedback = models.CharField(max_length=100, blank=True)

class UserFeedback(models.Model):
    regular_user_history = models.OneToOneField(RegularUserHistory, on_delete=models.PROTECT)
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, null=True, related_name='reason')
    other_feedback = models.ForeignKey(OtherFeedback, on_delete=models.CASCADE, related_name='other_reason', null=True)

class Image(models.Model):
    image = models.ImageField(upload_to='photo_post/')
    post = models.ForeignKey(Post, related_name='photos', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.image}, {self.post}"

class PostFollow(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(verbose_name='Active', default=True)
    post = models.ForeignKey(Post, related_name='followed', on_delete=models.CASCADE)
    follower = models.ManyToManyField(User, related_name='followers')

    def __str__(self):
        return f"{self.timestamp}, {self.is_active}, {self.post}, {self.follower}"