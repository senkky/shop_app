from django.contrib.auth.models import User
from django.db import models


def profile_images_directory_path(instance: "Profile", filename: str) -> str:
    return "profiles/profile_{pk}/avatar{filename}".format(
        pk=instance.user.pk,
        filename=filename,
    )


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(max_length=500, blank=True)
    agreement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(null=True, upload_to=profile_images_directory_path)

    @property
    def bio_short(self) -> str:
        if len(self.bio) < 48:
            return self.bio
        return self.bio[:48] + "..."

    def __str__(self) -> str:
        return f"Profile(pk={self.pk}, user={self.user!r}"
