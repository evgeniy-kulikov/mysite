from django.urls import path, re_path
from .views import PostList, PostDetail, UserPostList
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView  # Схемы и документация

# app_name = "blog_api"

urlpatterns = [
    path("<int:pk>/", PostDetail.as_view(), name="post_detail"),
    path("", PostList.as_view(), name="post_list"),
    re_path('^user/(?P<username>.+)/$', UserPostList.as_view()), # для фильтрации по URL
    path("schema/", SpectacularAPIView.as_view(), name="schema"),  # Динамическая схема
    path("schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),  # документация
    path("schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]

# http://127.0.0.1:8000/api/
# http://127.0.0.1:8000/api/user/10/
# http://127.0.0.1:8000/api/user/1/

#  http://127.0.0.1:8000/api/schema/  # Динамическая схема (файл для загрузки)
#  http://127.0.0.1:8000/api/schema/redoc/
#  http://127.0.0.1:8000/api/schema/swagger-ui/




