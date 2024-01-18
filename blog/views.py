from django.shortcuts import render, get_object_or_404
# from django.http import Http404

from .models import Post


def post_list(request):
    posts = Post.published.all()
    context = {'posts': posts}
    return render(request,
                  'blog/post/list.html',
                  context=context)


# Через функцию сокращенного доступа get_object_or_404()
def post_detail(request, id):
    post = get_object_or_404(Post,
                             id=id, status=Post.Status.PUBLISHED)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})


# Другой вариант вывода детальной записи
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
