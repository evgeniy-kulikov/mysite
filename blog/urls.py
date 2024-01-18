from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),

    # После применения в поле slug параметра unique_for_date="published" (модель Post)
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
          views.post_detail,
          name='post_detail'),
    # path('<int:id>/', views.post_detail, name='post_detail'),
]