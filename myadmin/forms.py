from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)

from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.utils.translation import gettext, gettext_lazy as _
from motels.models import User

class AccountAuthenticationForm(forms.ModelForm):

    email = forms.EmailField(
        label='', 
        max_length=255,
        error_messages={'invalid': 'Email không hợp lệ'}, 
        widget=forms.TextInput(attrs={'placeholder': 'Địa chỉ email'})
        )

    password = forms.CharField(
        label='', 
        widget=forms.PasswordInput(attrs={'placeholder': 'Mật khẩu'}),
        error_messages={'invalid': 'Không được để trống mật khẩu'}
        )

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']  
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Đăng nhập thất bại")
