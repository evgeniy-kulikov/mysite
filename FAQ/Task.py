# Answer
""""""


# 5.2 Создание моделей данных блога
"""
# Task 01
from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=50)
    age = models.PositiveIntegerField(default=18)
    address = models.TextField()
 
    
# Task 02
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)  
   
    
# Task 03
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)     
"""

# 5.4 Работа с наборами запросов QuerySet и менеджерами
""""
# Task 01
Article.objects.all()

# Task 02
Article.objects.get(id=5)

# Task 03
article = Article.objects.get(id=5)
article.delete()
или
Article.objects.get(id=5).delete()

# Task 04
Article.objects.order_by('-created')

# Task 05
Article.objects.filter(id=5).update(text="Django 4")

# Task 06
Article.objects.filter(created__year=2023)

# Task 07
Article.objects.exclude(created__year=2023)

# Task 08
Article.objects.filter(created__year=2022).filter(title__startswith='Django')

# Task 09
Article.objects.filter(id=5).update(title="Django 5", published=True)

# Task 10
post = Article(title='Django 5', description='Django 5 release notes', text='Expected December 2023')
post.save()

"""



# 6.5 Создание системы комментариев
"""
# Task 01
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField(default=0)

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    products = models.ManyToManyField(Product)
    
    
# Task 02
from django.db import models

class Album(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    description = models.TextField()
    release = models.DateField()
    price = models.PositiveIntegerField(default=0)
      
class Song(models.Model):
    title = models.CharField(max_length=100)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    
"""


