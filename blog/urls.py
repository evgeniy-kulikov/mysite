from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),  # форма отправки email

    # FBV
    # path('', views.post_list, name='post_list'),
    # Получение адреса через параметры publish.year/publish.month/publish.day/slug
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
          views.post_detail,
          name='post_detail'),

    path('<int:post_id>/comment/',
             views.post_comment, name='post_comment'),

    # Получение данных через id
    # path('<int:id>/', views.post_detail, name='post_detail'),
]