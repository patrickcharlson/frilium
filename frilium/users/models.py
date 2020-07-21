from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import TextChoices
from django.urls import reverse

from frilium.boards.models import Post, Topic


class User(AbstractUser):
    class Gender(TextChoices):
        NOT_SPECIFIED = '', 'Not Specified'
        MALE = 'Male', 'Male'
        FEMALE = 'Female', 'Female'

    username = models.CharField('Username', max_length=30, unique=True)
    bio = models.TextField('Bio', max_length=500, blank=True)
    location = models.CharField('Location', max_length=30, blank=True)
    gender = models.CharField('Gender', max_length=50, choices=Gender.choices, default=Gender.NOT_SPECIFIED)
    website = models.URLField('Website', max_length=30, blank=True)
    timezone = models.CharField('Time zone', max_length=32, default='UTC')
    name = models.CharField("Real name", blank=True, max_length=255)
    twitter = models.CharField('Twitter handle', max_length=20, blank=True)

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

    @property
    def last_post(self):
        posts = Post.objects.filter(created_by=self).order_by('-created_at')
        if posts:
            return posts[0].created_at
        else:
            return None
