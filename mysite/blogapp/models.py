from django.db import models
from django.utils.translation import gettext_lazy as _


class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Имя автора'))
    bio = models.TextField(verbose_name=_('Биография автора'))


class Category(models.Model):
    name = models.CharField(max_length=40, verbose_name=_('Название категории'))


class Tag(models.Model):
    name = models.CharField(max_length=20, verbose_name=_('Тэг статьи'))


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Заголовок статьи'))
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
