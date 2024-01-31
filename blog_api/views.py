from rest_framework import generics
from blog.models import Post
from .serializers import PostSerializer
from .permissions import IsAuthorOrReadOnly

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, permissions


# Чтобы изменить определенные аспекты стиля пагинации, переопределяем один из классов пагинации
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


# OrderingFilter
class PostList(generics.ListCreateAPIView):
    permission_classes = (IsAuthorOrReadOnly,)  # разрешения через переопределенный класс IsAuthorOrReadOnly
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author']
    search_fields = ['body', 'author__username']
    ordering_fields = ['author_id', 'publish']
    # ordering_fields = '__all__'  # упорядочивание по любому полю модели
    # ordering = ['body']  # строка, или спискок/кортеж строк
    pagination_class = StandardResultsSetPagination


# # SearchFilter
# class PostList(generics.ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter]
#     filterset_fields = ['author']
#     search_fields = ['body']



# class PostList(generics.ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     # модельное поле, которое используется для поиска объектов отдельных экземпляров модели. По умолчанию 'pk'
#     # lookup_field = 'pk'
#     filter_backends = [DjangoFilterBackend]  # pip django_filters
#     filterset_fields = ['author']  # pip django_filters
#
#     """
#     При необходимости можно сделать добавление фильтрации
#     Самый простой способ отфильтровать QuerySet любого представления, подкласса GenericAPIView,
#     - это переопределить метод .get_queryset()
#     """
#     # Отфильтровать набор запросов по текущему аутентифицированному пользователю
#     def get_queryset(self):
#         user = self.request.user
#         return Post.objects.filter(author=user)



# Набор постов, отфильтрованный по имени пользователя в части URL:
class UserPostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.kwargs['username']
        # user = self.kwargs['id']
        return Post.objects.filter(author=user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly,)  # разрешения через переопределенный класс IsAuthorOrReadOnly
    # permission_classes = (permissions.IsAdminUser,)  # Разрешения на уровне представлений
    queryset = Post.objects.all()
    serializer_class = PostSerializer
