from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class TypeRoom(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(max_length=400)

    class Meta:
        verbose_name = 'type of room'


class Housing(models.Model):
    address = models.CharField(max_length=100, verbose_name="address")
    type_room = models.ForeignKey(TypeRoom, on_delete=models.PROTECT, verbose_name="type of room")
    number_rooms = models.IntegerField(default=1, verbose_name="number of rooms")
    total_area = models.IntegerField(verbose_name="total area")

    class Meta:
        verbose_name_plural = 'housing'

    def get_absolute_url(self):
        return reverse('app_house:house', args=[str(self.id)])


class News(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="author")
    heading = models.CharField(max_length=150, verbose_name='heading')
    text = models.TextField(max_length=500)
    published = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'news'

    def get_absolute_url(self):
        return reverse('app_house:news', args=[str(self.id)])
