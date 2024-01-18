from django.shortcuts import render, get_object_or_404
# from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post


def post_list(request):
    posts_all = Post.published.all()
    # posts = Post.objects.all()

    # экземпляр класса Paginator с числом объектов (3), возвращаемых в расчете на страницу
    paginator = Paginator(posts_all, 3)
    # загрузить первую (по умолчанию) страницу результатов.
    page_number = request.GET.get('page', 1)

    try:
        # передаем номер страницы и объект posts в шаблон
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # Если page_number не целое число, то
        # выдать первую страницу
        posts = paginator.page(1)
    except EmptyPage:  # Пустая страница
        # Если page_number находится вне диапазона, то
        # выдать последнюю страницу
        posts = paginator.page(paginator.num_pages)

    context = {'posts': posts}
    return render(request,
                  'blog/post/list.html',
                  context=context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})

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
