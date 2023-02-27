from django.contrib.auth.models import User
from django.db import models
from django import forms


class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=30)
    create_data_time = models.DateTimeField(auto_now_add=True)
    articles = models.TextField(max_length=10000)
    gallere = models.ImageField(blank=True)
    archived = models.BooleanField(default=False)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField()
