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

# Добавление карты сайта
# https://docs.djangoproject.com/en/4.2/ref/contrib/sitemaps/
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
sitemaps = {'posts': PostSitemap,}


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('blog/', include('blog.urls', namespace='blog')),
    path('', include('blog.urls', namespace='blog')),  # путь blog/ временно убран для удобства

    # Добавление карты сайта  http://127.0.0.1:8000/sitemap.xml
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps},
    name="django.contrib.sitemaps.views.sitemap",),
]
# http://localhost:8000/2024/1/24/getting-the-gist-of-markdowns-formatting-syntax/