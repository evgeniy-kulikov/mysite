from django.urls import path
from .views import SignUpView, logout_view

app_name = 'accounts'

urlpatterns = [
    path("logout/", logout_view, name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
]

# http://127.0.0.1:8000/accounts/logout/
# http://127.0.0.1:8000/accounts/signup/

# название папки и файла - для встроенного auth приложение
# http://127.0.0.1:8000/registration/login/
# http://127.0.0.1:8000/accounts/password_reset/
# http://127.0.0.1:8000/accounts/password_reset/done/
