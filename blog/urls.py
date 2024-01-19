from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),

    # FBV
    # path('', views.post_list, name='post_list'),
    # Получение адреса через параметры publish.year/publish.month/publish.day/slug
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
          views.post_detail,
          name='post_detail'),

    # Получение данных через id
    # path('<int:id>/', views.post_detail, name='post_detail'),
]