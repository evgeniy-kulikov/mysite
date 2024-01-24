from django import template
from blog.models import Post
from django.db.models import Count

from django.utils.safestring import mark_safe
import markdown

"""
Для того чтобы быть допустимой библиотекой тегов, 
в каждом содержащем шаблонные теги модуле должна быть определена переменная с именем register.

Эта переменная является экземпляром класса template.Library, 
и она используется для регистрации шаблонных тегов и фильтров приложения.

Прежде чем использовать конкретно-прикладные шаблонные теги, 
необходимо сделать их доступными для шаблона с помощью тега {% load имя_тега %}
"""

register = template.Library()

# Простой тег
# общее число опубликованных в блоге постов
@register.simple_tag
def total_posts():
    cnt = Post.published.count()
    return cnt



# Вложенный тег
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


# Шаблонный тега, возвращающий набор запросов
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate( total_comments=Count('comments')) \
               .order_by('-total_comments')[:count]


# Поддержка синтаксиса Markdown
# Для избежания конфликта имен функции имя nmarkdown_format
# Для удобства вызова, даем фильтру имя name='markdown_tag'
@register.filter(name='markdown_tag')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))