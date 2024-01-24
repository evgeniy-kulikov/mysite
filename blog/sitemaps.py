# Добавление карты сайта
# https://stepik.org/lesson/973398/step/1?unit=980250
# https://docs.djangoproject.com/en/4.2/ref/contrib/sitemaps/
# https://habr.com/ru/articles/530766/

from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated
