from django.db import models
from datetime import datetime
from datetime import timezone as tz
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# django-taggit  # функциональность тегирования
from taggit.managers import TaggableManager


# Менеджер, который извлекает все посты, имеющие статус PUBLISHED
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)
        # return super().get_queryset()\
        #               .filter(status=Post.Status.PUBLISHED)


# Посты (статьи)
class Post(models.Model):
    objects = models.Manager()  # менеджер, применяемый по умолчанию
    published = PublishedManager()  # Новый конкретно-прикладной менеджер

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Черновик'
        PUBLISHED = 'PB', 'Публикация'

    title = models.CharField(max_length=250, verbose_name="Заголовок")
    # unique_for_date=...  слаги являются уникальными в пределах даты публикации поста "publish"
    slug = models.SlugField(max_length=250, unique_for_date="publish", verbose_name="URL slug")
    # slug = models.SlugField(max_length=250, verbose_name="URL slug")
    body = models.TextField(verbose_name="Содержимое")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name="Автор")

    publish = models.DateTimeField(default=timezone.now, verbose_name="Дата публикации")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT , verbose_name="Статус")

    # https://django-taggit.readthedocs.io/en/latest/getting_started.html#settings
    tags = TaggableManager()  # Менеджер tags позволит добавлять, извлекать и удалять теги из объектов Post

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ['-publish']
        # Добавление индекса БД
        indexes = [
            models.Index(fields=['-publish']),
        ]

    # канонический URL-адрес объекта
    # После применения в поле slug параметра unique_for_date="publish"
    # Получение адреса через параметры publish.year/publish.month/publish.day/slug
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

    # Получение адреса через id
    # def get_absolute_url(self):
    #     return reverse('blog:post_detail',
    #                    args=[self.id])

    def __str__(self):
        return self.title


# Комментарии
class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             # null=True,
                             related_name='comments')
    name = models.CharField(max_length=80, verbose_name="Пользователь")
    email = models.EmailField()
    body = models.TextField(verbose_name="Сообщение")
    created = models.DateTimeField(auto_now_add=True,  verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    active = models.BooleanField(default=True, verbose_name="Видимость")

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def when_published(self):
        """
        Информация о давности комментария
        Этот метод может быть заменен фильтром |timesince
        """
        now = datetime.now(tz.utc)
        diff = now - self.created

        # 0 day to 30 days
        if diff.days < 30:
            days = diff.days
            if days == 1:
                return str(days) + " day ago"
            else:
                return str(days) + " days ago"

        # 31 day to 365 days
        if diff.days >= 30 and diff.days < 365:
            months = diff.days // 30
            if months == 1:
                return str(months) + " month ago"
            else:
                return str(months) + " months ago"

        # 365+
        if diff.days >= 365:
            years = diff.days // 365
            if years == 1:
                return str(years) + " year ago"
            else:
                return str(years) + " years ago"


    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
