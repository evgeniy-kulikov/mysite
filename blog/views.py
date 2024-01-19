from django.shortcuts import render, get_object_or_404
# from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Post


# Переопределние класса Paginator
"""
При превышении диапазона страниц - выдает последнюю
При занижении (ноль и минус) диапазона страниц - выдает первую
При нечисловом значении выдает ошибку 404
"""
class MyPaginator(Paginator):
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
