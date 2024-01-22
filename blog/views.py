from django.shortcuts import render, get_object_or_404
# from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Post
from .forms import EmailPostForm, CommentForm
# работа с email
from django.core.mail import send_mail
from django.conf import settings

from django.views.decorators.http import require_POST


# Переопределние класса Paginator
class MyPaginator(Paginator):
    """
    При превышении диапазона страниц - выдает последнюю
    При занижении (ноль и минус) диапазона страниц - выдает первую
    При нечисловом значении выдает ошибку 404
    """

    def validate_number(self, number):
        try:
            return super().validate_number(number)
        except EmptyPage:
            if int(number) > 1:
                # return the last page
                return self.num_pages
            elif int(number) < 1:
                # return the first page
                return 1
            else:
                raise


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'
    paginator_class = MyPaginator


# При неверных номерах страницы выдает ошибку 404
# class PostListView(ListView):
#     # model = Post  # Будет выборка Post.objects.all()
#     queryset = Post.published.all() # Своя выборка
#     # Свое наименование, вместо умолчальной object_list
#     context_object_name = 'posts'
#     paginate_by = 3
#     # Шаблон по умолчанию  blog/post_list.html
#     template_name = 'blog/post/list.html'


""" FBV """


def post_share(request, post_id):
    """
    Рекомендация постов по электронной почте
    """
    # Извлечь пост по идентификатору id
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    sent = False
    """
    Если sent = False, то в шаблоне "../share.html" отражается форма отправки письма. 
    Если письмо было успешно отправлено, то sent = True и возвращаясь обратно на "../share.html"
    форма отправки письма скрывается и показывается текст об успешной отправки.
    """
    if request.method == 'POST':
        # Форма передается на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Поля формы успешно прошли валидацию
            cd = form.cleaned_data
            # отправить электронное письмо
            # build_absolute_uri() строит полный адрес включая доменное имя
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} Рекомендуем прочитать пост: {post.title}"
            message = f"Прочтите \"{post.title}\" по ссылке {post_url}\n\n" \
                      f"{cd['name']} ({cd['email']}) сообщает: {cd['comments']}"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})


@require_POST  # представление принимает только метод POST
def post_comment(request, post_id):
    """
    Комментирование постов
    """
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)

    # для хранения комментарного объекта при его создании
    comment = None

    # Комментарий был отправлен
    form = CommentForm(data=request.POST)

    if form.is_valid():
        # Создать объект класса Comment, не сохраняя его в базе данных (commit=False)
        comment = form.save(commit=False)

        # Назначить пост комментарию
        comment.post = post

        # Сохранить комментарий в базе данных
        comment.save()
    return render(request, 'blog/post/comment.html',
                  {'post': post,
                   'form': form,
                   'comment': comment})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    # Список активных комментариев к этому посту
    # comment_order - сортировка комментариев по возрастанию / убыванию по дате публикации
    comment_order = 'created'
    if 'desc' in request.GET:  # кнопка <button name="desc">По убыванию</button> на 'blog/post/detail.html'
        comment_order = '-created'
    elif 'asc' in request.GET:
        comment_order = 'created'

    # comments это  related_name='comments'  поля "post" таблицы "Comment"
    comments_list = post.comments.filter(active=True).order_by(comment_order)

    # Форма для комментирования пользователями
    form = CommentForm()
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments_list,
                   'form': form})



# Получение данных через дату и слаг
# def post_detail(request, year, month, day, post):
#     post = get_object_or_404(Post,
#                              status=Post.Status.PUBLISHED,
#                              slug=post,
#                              publish__year=year,
#                              publish__month=month,
#                              publish__day=day)
#     return render(request,
#                   'blog/post/detail.html',
#                   {'post': post})

# Через функцию сокращенного доступа get_object_or_404()
# Получение данных через id
# def post_detail(request, id):
#     post = get_object_or_404(Post,
#                              id=id, status=Post.Status.PUBLISHED)
#     return render(request,
#                   'blog/post/detail.html',
#                   {'post': post})


# Другой вариант вывода детальной записи
# Получение данных через id
# def post_detail(request, id):
#     try:
#         post = Post.published.get(id=id)
#
#     except Post.DoesNotExist:
#         raise Http404("No Post found.")
#
#     return render(request,
#                   'blog/post/detail.html',
#                   {'post': post})


"""  * * *   Переделано на CBV   *  *  *   """
# def post_list(request):
#     posts_all = Post.published.all()
#     # posts = Post.objects.all()
#
#     # экземпляр класса Paginator с числом объектов (3), возвращаемых в расчете на страницу
#     paginator = Paginator(posts_all, 3)
#     # загрузить первую (по умолчанию) страницу результатов.
#     page_number = request.GET.get('page', 1)
#
#     try:
#         # передаем номер страницы и объект posts в шаблон
#         posts = paginator.page(page_number)
#     except PageNotAnInteger:
#         # Если page_number не целое число, то
#         # выдать первую страницу
#         posts = paginator.page(1)
#     except EmptyPage:  # Пустая страница
#         # Если page_number находится вне диапазона, то
#         # выдать последнюю страницу
#         posts = paginator.page(paginator.num_pages)
#
#     context = {'posts': posts}
#     return render(request,
#                   'blog/post/list.html',
#                   context=context)
