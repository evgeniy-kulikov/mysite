from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from accounts.models import Profile

from django_summernote.widgets import SummernoteWidget  # Редактор Summernote


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, label='Имя')
    last_name = forms.CharField(max_length=100, label='Фамилия')
    username = forms.CharField(max_length=30, label='Логин')
    email = forms.EmailField(max_length=200)
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(), label='Пароль')
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(), label='Повторить пароль')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput())
    email = forms.EmailField(required=True,
                             widget=forms.TextInput())

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput())

    # bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))  # простое поле
    bio = forms.CharField(widget=SummernoteWidget())  # виджет редактора Summernote
    # переопределить настройки из SUMMERNOTE_CONFIG
    # bio = forms.CharField(widget=SummernoteWidget(attrs={'summernote': {'width': '50%', 'height': '400px'}}))  # виджет редактора Summernote


    class Meta:
        model = Profile
        fields = ['avatar', 'bio']