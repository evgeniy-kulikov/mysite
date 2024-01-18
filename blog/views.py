from django.shortcuts import render, get_object_or_404
# from django.http import Http404

from .models import Post


def post_list(request):
    posts = Post.published.all()
    # posts = Post.objects.all()
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
