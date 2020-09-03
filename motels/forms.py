from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Post, Province, Room
from django.core.exceptions import ValidationError
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)

from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.utils.translation import gettext, gettext_lazy as _

class RegisterForm(UserCreationForm):
    last_name = forms.CharField(label='', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Họ', 'autocomplete':'off'}))
    first_name = forms.CharField(label='', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Tên', 'autocomplete':'off'}))
    email = forms.EmailField(label='', max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Địa chỉ email', 'autocomplete':'off'}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Mật khẩu mới', 'autocomplete':'off'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Nhập lại mật khẩu', 'autocomplete':'off'}))

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'email', 'password1', 'password2')
        

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
                raise forms.ValidationError("Email hoặc mật khẩu của bạn không đúng, vui lòng thử lại")

class UpdateProfileForm(forms.ModelForm):
    last_name = forms.CharField(label='', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Họ', 'autocomplete':'off'}))
    first_name = forms.CharField(label='', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Tên', 'autocomplete':'off'}))
    address = forms.ModelChoiceField(label='', queryset=Province.objects.all(), empty_label="-----------")

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'address')
            
class SetPasswordFormChild(SetPasswordForm):
    error_messages = {
        'password_mismatch': _('Mật khẩu mới nhập lại không khớp.'),
    }
    new_password1 = forms.CharField(
        label=_("Mật khẩu mới"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=(
            'Mật khẩu không được quá phổ biến hay giống với các thông tin cá nhân khác của bạn, cần chứa ít nhất 8 ký tự không hoàn toàn bằng số.'
            )
    )
    new_password2 = forms.CharField(
        label=_("Nhập lại mật khẩu mới"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(user, *args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user

class MyChangeFormPasswordChild(SetPasswordFormChild, PasswordChangeForm):
    error_messages = {
        **SetPasswordFormChild.error_messages,
        'password_incorrect': _("Mật khẩu cũ bạn vừa nhập không chính xác, vui lòng nhập lại."),
    }
    old_password = forms.CharField(
        label=_("Mật khẩu cũ"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
    )
    

class RUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'address', 'avatar')