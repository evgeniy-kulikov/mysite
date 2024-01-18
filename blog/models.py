from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Менеджер, который извлекает все посты, имеющие статус PUBLISHED
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)
        # return super().get_queryset()\
        #               .filter(status=Post.Status.PUBLISHED)


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

