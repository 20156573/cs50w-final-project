from django import forms
from django.db.models import Count
from django.utils import timezone
from django.db import models, transaction, IntegrityError
from django.forms import widgets
from django.conf.urls import url
from django.urls import reverse
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.widgets import AdminFileWidget
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User, Post, PostAddress, House, Room, Roommate, Apartment, Image, PostStatus, RegularUserHistory
from django.urls import path
from django.shortcuts import HttpResponse, HttpResponseRedirect, redirect
from django.template.response import TemplateResponse

# Overriding

class CategoryListFilter(SimpleListFilter):
    
    title = _('Loại bài đăng')
    parameter_name = 'cate'
    def lookups(self, request, model_admin):
        
        return (
            ('0', _('Tìm người ở ghép')),
            ('1', _('Cho thuê phòng trọ')),
            ('2', _('Cho thuê nhà nguyên căn')),
            ('3', _('Cho thuê nguyên căn chung cư')),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(category=self.value())
        return queryset

class AdminImageWidget(AdminFileWidget):

    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name=str(value)
            output.append(u' <a href="%s" target="_blank"><img src="%s" alt="%s" width="150" height="150"  style="object-fit: cover;"/></a> %s ' %\
                (image_url, image_url, file_name, _('')))
    
        output.append(super(AdminFileWidget, self).render(name, value, attrs))  
        return mark_safe(u''.join(output))

# Inline
class AddressInline(admin.StackedInline):
    model = PostAddress
    extra = 0 
    can_delete = False
    max_num=0

class RoomateInline(admin.StackedInline):
    model = Roommate
    extra = 0 
    can_delete = False
    max_num=0

class RoomInline(admin.StackedInline):
    model = Room
    extra = 0 
    can_delete = False
    max_num=0

class ApartmentInline(admin.StackedInline):
    model = Apartment
    extra = 0 
    can_delete = False
    max_num=0

class HouseInline(admin.StackedInline):
    model = House
    extra = 0 
    can_delete = False
    max_num=0

class PostInline(admin.StackedInline):
    model = Post
    extra = 0 
    can_delete = False
    max_num=0
    # def formfield_for_dbfield(self, db_field, request, **kwargs):
    #     form = super(PostInline, self).formfield_for_dbfield(db_field, request, **kwargs)
    #     form.widget.can_add_related = False
    #     return form

class ImageInline(admin.TabularInline):
    model = Image
    extra = 0
    can_delete = True
    # max_num=0

    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget}
    }

    
# User
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm): 
    password = ReadOnlyPasswordHashField()
    
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')

    def clean_password(self):
        return self.initial["password"]

class UserAdmin(BaseUserAdmin):
    model = User
    form = UserChangeForm
    add_form = UserCreationForm

    # inlines = [PostInline]
   
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(number_post=Count('posts')).order_by('-number_post')
        return qs

    def number_post(self, obj):
        return obj.posts.count()

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser == True:
            return True
            
        return False
    def image_tag(self, obj):
        return format_html('<img src="{}" width="40px" height="40px" style="border-radius: 50%; object-fit:cover;"/>'.format(obj.avatar.url))

    list_display = ('email', 'full_name', 'is_superuser', 'is_staff', 'is_active', 'image_tag', 'number_post')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    readonly_fields=('date_joined', 'image_tag',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'image_tag')}),
        ('Thông tin cá nhân', {'fields': (('first_name', 'last_name', 'address'),'avatar', )}),
        ('Quyền', {'fields': ('is_superuser', 'is_staff','is_active')}),
        ('Mốc thời gian', {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email', 'first_name', 'last_name',)
    number_post.admin_order_field = 'number_post'
    number_post.short_description = 'Số tin đã đăng'
    image_tag.short_description = 'Ảnh đại diện'

class PostAdmin(admin.ModelAdmin):
    # exclude = ('title', ) Không show một trường nào đó ra

    inlines = (RoomateInline, ImageInline, RoomInline, ImageInline, ApartmentInline, ImageInline, HouseInline, ImageInline)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def image_tag(self, obj):
        return format_html('<p>{}</p>'.format(PostAddress.objects.select_related('post').filter(post=obj).first()))
    
    def get_inline_instances(self, request, obj=None):
        return [inline(self.model, self.admin_site) for inline in self.inlines[obj.category:obj.category+2]]
    

    model = Post
    fieldsets = (
        ('Thông tin cơ bản', {'fields': ('title', 'category', 'description', 'area', 'renters_gender', 'furniture', 'image_tag')}),
        ('Thông tin liên hệ', {'fields': ('poster', 'other_contact_info')}),
        ('Thông tin thuê nhà', {'fields': ('rent', 'deposit')}),
    )
    search_fields = ('title', 'id')
    readonly_fields = ('category', 'image_tag',)
    list_display = ('title', 'update_time', 'getCategory', 'category') #Các trường hiển thị nhanh
    list_filter = ('update_time', CategoryListFilter, 'category')  
    image_tag.short_description = 'Ảnh đại diện'

class RegularUserHistoryAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False


    def get_urls(self):
        urls = super(RegularUserHistoryAdmin, self).get_urls()

        security_urls = [
            url(r'^approval/$', self.admin_site.admin_view(self.get_post)),
            url(r'^approved/$', self.admin_site.admin_view(self.get_post_approved)),
            url(r'^not_approved/$', self.admin_site.admin_view(self.get_post_not_approved)),
            url(r'^approval/post$', self.admin_site.admin_view(self.approval)),
            url(r'^hidden/$', self.admin_site.admin_view(self.get_post_hidden)),
        ]
        return security_urls + urls

    # Your view definition fn
    def get_post(self, request):
        p = request.GET.get('p', '')

        hh = RegularUserHistory.objects.raw("select * from (select distinct on (his.post_id) his.post_id, p.poster_id, his.created_at, his.id, p.title, u.email, p.category from \
            motels_regularuserhistory as his join motels_post as p on p.id = his.post_id and p.status = 1 join motels_user as u on\
                u.id = p.poster_id where (UPPER(p.title) \
                LIKE UPPER(%s) OR UPPER(u.email) LIKE UPPER(%s)) order by \
                his.post_id, his.id desc) as ds order by ds.created_at desc", ('%' + p + '%', '%' + p + '%'))
                
        context = dict(
            self.admin_site.each_context(request), # Include common variables for rendering the admin template.
            hh=hh,
        )
        return TemplateResponse(request, "approval/index.html", context)

    def get_post_approved(self, request):
        p = request.GET.get('p', '')

        hh = RegularUserHistory.objects.raw("select * from (select distinct on (his.post_id) his.post_id, p.poster_id, his.updated_by_id \
            ,(select concat(a.first_name,' ', a.last_name,' > ', a.email) from motels_user as a where a.id = his.updated_by_id) as updated_by_info,\
            his.created_at, his.id, p.title, u.email, p.category from \
            motels_regularuserhistory as his join motels_post as p on p.id = his.post_id and (p.status = 2 or p.status = 7) join motels_user as u on\
            u.id = p.poster_id where (UPPER(p.title) \
            LIKE UPPER(%s) OR UPPER(u.email) LIKE UPPER(%s)) order by \
            his.post_id, his.id desc) as ds order by ds.created_at desc", ('%' + p + '%', '%' + p + '%'))
                
        context = dict(
            self.admin_site.each_context(request), # Include common variables for rendering the admin template.
            hh=hh,
        )
        return TemplateResponse(request, "approval/approved.html", context)
    
    def get_post_not_approved(self, request):
        p = request.GET.get('p', '')

        hh = RegularUserHistory.objects.raw("select * from (select distinct on (his.post_id) his.post_id, p.poster_id, his.updated_by_id \
            ,(select concat(a.first_name,' ', a.last_name,' > ', a.email) from motels_user as a where a.id = his.updated_by_id) as updated_by_info,\
            his.created_at, his.id, p.title, u.email, p.category from \
            motels_regularuserhistory as his join motels_post as p on p.id = his.post_id and p.status = 3 join motels_user as u on\
            u.id = p.poster_id where (UPPER(p.title) \
            LIKE UPPER(%s) OR UPPER(u.email) LIKE UPPER(%s)) order by \
            his.post_id, his.id desc) as ds order by ds.created_at desc", ('%' + p + '%', '%' + p + '%'))
                
        context = dict(
            self.admin_site.each_context(request), # Include common variables for rendering the admin template.
            hh=hh,
        )
        return TemplateResponse(request, "approval/not_approved.html", context)

    def get_post_hidden(self, request):
        p = request.GET.get('p', '')

        hh = RegularUserHistory.objects.raw("select * from (select distinct on (his.post_id) his.post_id, p.poster_id, his.updated_by_id \
            ,a.is_superuser, a.is_staff, concat(a.first_name,' ', a.last_name,' > ', a.email) as updated_by_info,\
            his.created_at, his.id, p.title, u.email, p.category from \
            motels_regularuserhistory as his join motels_post as p on p.id = his.post_id and (p.status = 6 or p.status = 5) join motels_user as u on\
            u.id = p.poster_id join motels_user as a on a.id = his.updated_by_id where (UPPER(p.title)  \
            LIKE UPPER(%s) OR UPPER(u.email) LIKE UPPER(%s)) order by \
            his.post_id, his.id desc) as ds order by ds.created_at desc", ('%' + p + '%', '%' + p + '%'))
                
        context = dict(
            self.admin_site.each_context(request), # Include common variables for rendering the admin template.
            hh=hh,
        )
        return TemplateResponse(request, "approval/hidden.html", context)

    @transaction.atomic
    @csrf_exempt
    def approval(self, request):
        context = dict(
            self.admin_site.each_context(request), 
        )
        if request.method == 'POST':
            action = request.POST['type']
            checked = request.POST['checked'].split(',')
            
            if action == '#deny':
                for c in checked:
                    p = Post.objects.get(pk=int(c))
                    try:
                        status = PostStatus.objects.get(pk=3)
                        h = RegularUserHistory(status=status, post=p, updated_by=request.user)
                        p.status = 3
                        p.update_time=timezone.now()
                        p.save()
                        h.save()
                    except IntegrityError as e:
                        print(e)
                return HttpResponseRedirect('../approval/')
            if action == '#addlink':
                for c in checked:
                    p = Post.objects.get(pk=int(c))
                    try:
                        status = PostStatus.objects.get(pk=2)
                        h = RegularUserHistory(status=status, post=p, updated_by=request.user)
                        p.status = 2
                        p.update_time=timezone.now()
                        p.save()
                        h.save()
                    except IntegrityError as e:
                        print(e)
                return HttpResponseRedirect('../approval/')
            if action == '#hidden':
                for c in checked:
                    p = Post.objects.get(pk=int(c))
                    try:
                        status = PostStatus.objects.get(pk=5)
                        h = RegularUserHistory(status=status, post=p, updated_by=request.user)
                        p.status = 5
                        p.update_time=timezone.now()
                        p.save()
                        h.save()
                    except IntegrityError as e:
                        print(e)
                return HttpResponseRedirect('../approved/')

            if action == '#shown':
                for c in checked:
                    p = Post.objects.get(pk=int(c))
                    try:
                        status = PostStatus.objects.get(pk=7)
                        h = RegularUserHistory(status=status, post=p, updated_by=request.user)
                        p.status = 7
                        p.update_time=timezone.now()
                        p.save()
                        h.save()
                    except IntegrityError as e:
                        print(e)
                return HttpResponseRedirect('../hidden/')

                

            # return HttpResponse(checked)
        



admin.site.site_header = 'Raonhatro'
admin.site.register(Post, PostAdmin)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(RegularUserHistory, RegularUserHistoryAdmin)