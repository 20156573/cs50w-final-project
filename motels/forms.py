from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import User, Post, Province

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
        error_messages={'invalid': 'Không được để trống mật kh'}
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