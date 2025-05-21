from django.db import models
from accounts.models import CustomUser


class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    tags = models.CharField(max_length=255, help_text="Разделяй теги запятыми")
    youtube_url = models.URLField()

    def __str__(self):
        return self.title

class Rating(models.Model):
    LIKE = 'like'
    DISLIKE = 'dislike'
    RATING_CHOICES = [(LIKE, '👍 Лайк'), (DISLIKE, '👎 Дизлайк')]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    value = models.CharField(max_length=7, choices=RATING_CHOICES)


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} - избранное: {self.video.title}"
class ViewLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} смотрел {self.video.title}"

# Create your models here.
