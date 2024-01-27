from django.urls import path
from .views import SignUpView, logout_view, CustomLoginView, profile, ChangePasswordView
from django.contrib.auth import views as auth_views


app_name = 'accounts'

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),

    # redirect_authenticated_user=True
    # означает, что пользователи, пытающиеся получить доступ к странице входа после аутентификации,
    # будут перенаправлены обратно.
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True,
                                           template_name='registration/login.html'), name='login'),

    # На Django 5.0 и выше  удалили выход из системы по запросу GET
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),

    # Для Django 5.0 и выше
    # path("logout/", logout_view, name="logout"),

    path('profile/', profile, name='users-profile'),
    path('password_change/', ChangePasswordView.as_view(), name='password_change'),
]



# http://127.0.0.1:8000/accounts/logout/
# http://127.0.0.1:8000/accounts/signup/   # регистрация нового пользователя

# название папки и файла - для встроенного auth приложение
# http://127.0.0.1:8000/registration/login/
# http://127.0.0.1:8000/accounts/password_reset/
# http://127.0.0.1:8000/accounts/password_reset/done/

