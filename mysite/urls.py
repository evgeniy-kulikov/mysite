"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.urls import re_path

# Добавление карты сайта
# https://docs.djangoproject.com/en/4.2/ref/contrib/sitemaps/
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
sitemaps = {'posts': PostSitemap,}

# для возможности отображения медиафайлов
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    # path('blog/', include('blog.urls', namespace='blog')),
    path('', include('blog.urls', namespace='blog')),  # путь blog/ временно убран для удобства

    # Добавление карты сайта  http://127.0.0.1:8000/sitemap.xml
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps},
    name="django.contrib.sitemaps.views.sitemap",),

    #  собственное приложение
    path("accounts/", include("accounts.urls")),
    #  встроенное auth приложение
    path("accounts/", include("django.contrib.auth.urls")),

    re_path(r'^oauth/', include('social_django.urls', namespace='social')),  # OAuth 2.0
    path('summernote/', include('django_summernote.urls')), # добавление редактора summernote

    path("api/", include("blog_api.urls")),  # Django REST Framework

]

if settings.DEBUG:
    # # Django Debug Toolbar
    # urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
    # для возможности отображения медиафайлов в режиме DEBUG
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
URL-адреса, предоставленные auth:

accounts/login/ [name='login']
accounts/logout/ [name='logout']
accounts/password_change/ [name='password_change']
accounts/password_change/done/ [name='password_change_done']
accounts/password_reset/ [name='password_reset']
accounts/password_reset/done/ [name='password_reset_done']
accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/reset/done/ [name='password_reset_complete']
"""

# Проверка отображения языка Markdown
# http://localhost:8000/2024/1/24/getting-the-gist-of-markdowns-formatting-syntax/
