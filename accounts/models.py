from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ADMIN = "Admin"
    DRIVER = "Driver"
    USER_TYPES = [
        (ADMIN, "Admin"),
        (DRIVER, "Driver"),
    ]

    # fields
    user_type = models.CharField(max_length=32, choices=USER_TYPES, default=DRIVER)
