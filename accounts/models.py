from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbsctractBaseUser
from django.contrib.auth.models import Group, Permission

# Create your models here.

class CustomUserManager(BaseUserManager):

    def create_user(self, username, password, **kwargs):
        user = CustomUser(
            username = username,
        )
        user.set_password(password)
        user.save()

    def create_superuser(self, username, password, **kwargs):
        user = CustomUser(
            username = username,
            is_staff = True,
            is_superuser = True,
            user_type = CustomUser.ADMIN,
        )
        user.set_password(password)
        user.save()


class CustomUser(AbstractBaseUser):
    ADMIN = "Admin"
    DRIVER = "Driver"
    USER_TYPES = [
        (ADMIN, "Admin"),
        (DRIVER, "Driver"),
    ]

    # fields
    username = models.CharField(max_length=64, unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField()
    password = models.CharField(max_length=64)
    user_type = models.CharField(max_length=32, choices=USER_TYPES)
    is_staff = models.BooleanField(null=False, default=False)
    is_superuser = models.BooleanField(null=False, default=False)
    groups = models.ManyToManyField(Group)
    user_permissions = models.ManyToManyField(Permission)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
