from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


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