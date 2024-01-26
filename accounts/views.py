from django.shortcuts import render

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect

from django.contrib.auth import logout

from .forms import SignUpForm

class SignUpView(generic.CreateView):
    # form_class = UserCreationForm  # встроенный класс из auth.forms
    form_class = SignUpForm  # переопределили UserCreationForm из встроенного класса auth.forms
    success_url = reverse_lazy("login")  # Перенаправление на login-страницу при успешной регистрации
    template_name = "accounts/signup.html"


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(redirect_to=reverse('blog:post_list'))
