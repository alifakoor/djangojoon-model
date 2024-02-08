from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models


class User(AbstractUser):
    followings = models.ManyToManyField("self", symmetrical=False)
    bio = models.CharField(max_length=150, blank=True, null=True)
    profile_image = models.FileField(
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg"])],
        blank=True,
        null=True,
    )

    def display_name(self):
        if self.first_name.strip() and self.last_name.strip():
            return f"{self.first_name} {self.last_name}"
        else:
            return self.username
