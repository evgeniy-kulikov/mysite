from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),  # Список постов
    # Список постов отфильтрованных по тегам
    path('tag/<slug:tag_slug>/',views.PostListView.as_view(), name='post_list_by_tag'),

    path('<int:post_id>/share/', views.post_share, name='post_share'),  # форма отправки email


    # FBV
    # Переделано на CBV
    # path('', views.post_list, name='post_list'),
    # path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),

    # Получение адреса через параметры publish.year/publish.month/publish.day/slug
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
          views.post_detail,
          name='post_detail'),

    path('<int:post_id>/comment/',
             views.post_comment, name='post_comment'),

    # Получение данных через id
    # path('<int:id>/', views.post_detail, name='post_detail'),
]