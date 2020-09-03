from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib import messages

from .models import CardHistory, CardAmount, CardType

class RechargeForm(forms.ModelForm):
    telco = forms.ModelChoiceField(label='Nhà mạng', queryset=CardType.objects.all(), widget=forms.RadioSelect, empty_label=None)
    declared_value = forms.ModelChoiceField(label='Mệnh giá', queryset=CardAmount.objects.all(), empty_label='Mệnh giá')

    class Meta:
        model = CardHistory
        fields = ('serial', 'telco', 'declared_value', 'code')

    def clean(self):
        if self.is_valid():
            code = self.cleaned_data['code']  
            serial = self.cleaned_data['serial']
            telco = self.cleaned_data['telco']
            his = CardHistory.objects.filter(code=code).filter(serial=serial).filter(telco=telco)
            if len(his) != 0:
                his = his.first()
                if his.status == 99:
                    raise forms.ValidationError("Thẻ này đã được yêu cầu và đang chờ được xử lý")
                if his.status == 1 or  his.status == 2 or  his.status == 3:
                    raise forms.ValidationError("Thẻ này đã được sử dụng, vui lòng chọn thẻ khác")
        # raise forms.ValidationError("Vui lòng nhập đủ tất cả các trường")

            

            
        