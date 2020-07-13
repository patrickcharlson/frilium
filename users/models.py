from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from boards.models import Post, Topic


class User(AbstractUser):
    username = models.CharField('Username:', max_length=30, unique=True)

    def get_absolute_url(self):
        return reverse('users:user_profile', kwargs={'username': self.username})

    @property
    def post_count(self):
        return Post.objects.select_related().filter(created_by=self).count()

    @property
    def topic_count(self):
        return Topic.objects.select_related().filter(created_by=self).count()

    def posts_link(self):
        return reverse('users:user_posts', args=[self.username, self.pk])

    def topics_link(self):
        return reverse('users:user_topics', args=[self.username, self.pk])
