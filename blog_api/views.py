from rest_framework import generics
from blog.models import Post
from .serializers import PostSerializer

from django_filters.rest_framework import DjangoFilterBackend

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # модельное поле, которое используется для поиска объектов отдельных экземпляров модели. По умолчанию 'pk'
    # lookup_field = 'pk'
    filter_backends = [DjangoFilterBackend]  # pip django_filters
    filterset_fields = ['author']  # pip django_filters

    """ 
    При необходимости можно сделать добавление фильтрации 
    Самый простой способ отфильтровать QuerySet любого представления, подкласса GenericAPIView, 
    - это переопределить метод .get_queryset()
    """
    # Отфильтровать набор запросов по текущему аутентифицированному пользователю
    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author=user)



# Набор постов, отфильтрованный по имени пользователя в части URL:
class UserPostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.kwargs['username']
        # user = self.kwargs['id']
        return Post.objects.filter(author=user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer