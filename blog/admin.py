from django.contrib import admin
from blog.models import Post, Comment
# from taggit.models import TaggedItem
from django_summernote.admin import SummernoteModelAdmin  # редактор Summernote

# admin.site.register(Post)

@admin.register(Post)
# переопределили наследование нашего класса Post с интерфейса администратора по умолчанию, на SummernoteModelAdmin
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('body',)  # поля в каких необходим редактор Summernote
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    # поле author отображается поисковым виджетом, а не выпадающим списком (где много пользователей)
    raw_id_fields = ['author']
    date_hierarchy = 'publish'  # Выводимые поля групируются по датам публикации
    ordering = ['status', 'publish']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
    list_editable = ['active']


