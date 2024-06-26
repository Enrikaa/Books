from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = None
    last_name = None
    password_last_change = models.DateTimeField(null=True, blank=True)

