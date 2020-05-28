from django.contrib.auth.models import AbstractUser

from boards.models import Post, Topic


class User(AbstractUser):
    pass
