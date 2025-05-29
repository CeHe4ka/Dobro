from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    birth_date = models.DateField(null=True, blank=False)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # username обязательно

    def __str__(self):
        return self.email

    class Meta:
        permissions = [
            ("can_export_users", "Can export users to Excel"),
        ]


# Create your models here.
