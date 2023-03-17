from django.contrib.auth.models import User
from django.db import models


def blog_gallery_directory_path(instance: "Blog", filename: str) -> str:
    return "blog/blog_{id}/gallery{filename}".format(
        id=instance.user_id,
        filename=filename,
    )


class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=30)
    create_data_time = models.DateTimeField(auto_now_add=True, auto_now=False)
    articles = models.TextField(max_length=10000)
    archived = models.BooleanField(default=False)


class BlogGallery(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    gallery = models.ImageField(blank=True, upload_to=blog_gallery_directory_path)


def profile_images_directory_path(instance: "Profile", filename: str) -> str:
    return "profile/profile_{pk}/avatar{filename}".format(
        pk=instance.user.pk,
        filename=filename,
    )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to=profile_images_directory_path)
