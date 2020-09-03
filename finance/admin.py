from django.contrib import admin
from .models import CardHistory, Vip, Discount, PostedAds
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _
# Register your models here.

class HisStatusListFilter(SimpleListFilter):
    
    title = _('Trạng thái thẻ nạp')
    parameter_name = 'status'
    def lookups(self, request, model_admin):
        
        return (
            (99, _('Thẻ đang chờ xử lý')),
            (1, _('Thành công')),
            (2, _('Thành công nhưng sai mệnh giá')),
            (3, _('Thất bại')),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())
        return queryset


class CardHistoryAdmin(admin.ModelAdmin):
    model = CardHistory
    search_fields = ('code', 'serial', 'request_id')
    list_display = ('request_id', 'value', 'amount', 'telco', 'user', 'get_date', 'message')
    list_filter = ('timestamp', HisStatusListFilter, 'telco')  
    fieldsets = (
        ('', {'fields': ('telco', ('code', 'serial'))}),
        ('Finance', {'fields': ('value', 'amount')}),
        ('Status', {'fields': ('message',)}),
    )
    readonly_fields = ('telco', 'code', 'serial', 'message', 'value', 'amount')
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

    # def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
    #     extra_context = extra_context or {}
    #     extra_context['show_save_and_continue'] = False
    #     extra_context['show_save'] = False
    #     return super(CardHistoryAdmin, self).changeform_view(request, object_id, extra_context=extra_context)

    def change_view(self, request, object_id, extra_context=None):
        ''' customize add/edit form '''
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        return super(CardHistoryAdmin, self).change_view(request, object_id, extra_context=extra_context)
    
# class DiscountInline(admin.StackedInline):
#     model = Discount.vip.through
#     extra = 1

class VipAdmin(admin.ModelAdmin):
    # inlines = [DiscountInline]
    extra = 1

# class DiscountAdmin(admin.ModelAdmin):
#     filter_horizontal = ("vip",)

# class DiscountAdmin(admin.ModelAdmin):
    

admin.site.register(CardHistory, CardHistoryAdmin)
# admin.site.register(PostedAds, PostedAdsAdmin)
admin.site.register(Vip)
# admin.site.register(Discount, DiscountAdmin)
