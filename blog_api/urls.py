from django.urls import path, re_path
from .views import PostList, PostDetail, UserPostList

app_name = "blog_api"

urlpatterns = [
    path("<int:pk>/", PostDetail.as_view(), name="post_detail"),
    path("", PostList.as_view(), name="post_list"),
    re_path('^user/(?P<username>.+)/$', UserPostList.as_view()), # для фильтрации по URL
]

# http://127.0.0.1:8000/api/
# http://127.0.0.1:8000/api/user/10/
# http://127.0.0.1:8000/api/user/1/