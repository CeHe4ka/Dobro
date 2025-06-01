from django.db import models
from accounts.models import CustomUser
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    tags = models.CharField(max_length=255, help_text="Разделяй теги запятыми")
    youtube_url = models.CharField(max_length=255)
    duration = models.CharField(max_length=255, null=True, blank=True)
    age = models.CharField(max_length=255, null=True, blank=True)
    year = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        return self.title

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    value = models.CharField(max_length=10, choices=[('like', 'Like'), ('dislike', 'Dislike')], null=True, blank=True)
    is_favorite = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'video')


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} - избранное: {self.video.title}"
class ViewLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'video')

    def __str__(self):
        return f"{self.user.email} смотрел {self.video.title}"

# Create your models here.
class WatchLater(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'video')

    def __str__(self):
        return f"{self.user} -> {self.video} (Watch Later)"