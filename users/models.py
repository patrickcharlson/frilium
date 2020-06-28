import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.cache import cache
from django.urls import reverse

from boards.models import Post, Topic


class User(AbstractUser):

    def get_absolute_url(self):
        return reverse('users:user_profile', kwargs={'username': self.username})

    @property
    def post_count(self):
        return Post.objects.filter(created_by=self).count()

    @property
    def topic_count(self):
        return Topic.objects.filter(created_by=self).count()
