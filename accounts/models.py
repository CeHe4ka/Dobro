from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    birth_date = models.DateField(null=True, blank=False)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    is_editor = models.BooleanField(default=False)
    is_editor_request = models.BooleanField(default=False)
    editor_social_link = models.URLField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # username обязательно

    def __str__(self):
        return self.email

    class Meta:
        permissions = [
            ("can_export_users", "Can export users to Excel"),
        ]
