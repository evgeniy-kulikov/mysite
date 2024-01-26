from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect

from .forms import SignUpForm


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")

    # Через метод initial мы можем передать словарь
    # с ключами - именами полей и значениями - начальными значениями полей формы.
    initial = None  # принимает {'key': 'value'}

    template_name = 'accounts/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Создан аккаунт для {username}')

            return redirect(to='/')
        return render(request, self.template_name, {'form': form})

# # Простой вариант
# class SignUpView(generic.CreateView):
#     # form_class = UserCreationForm  # встроенный класс из auth.forms
#     form_class = SignUpForm  # переопределили UserCreationForm из встроенного класса auth.forms
#     success_url = reverse_lazy("login")  # Перенаправление на login-страницу при успешной регистрации
#     template_name = "accounts/signup.html"


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(redirect_to=reverse('blog:post_list'))
