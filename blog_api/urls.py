from django.urls import path
from .views import PostList, PostDetail

app_name = "blog_api"

urlpatterns = [
    path("<int:pk>/", PostDetail.as_view(), name="post_detail"),
    path("", PostList.as_view(), name="post_list"),
]

# http://127.0.0.1:8000/api/