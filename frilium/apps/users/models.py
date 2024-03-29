from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import TextChoices
from django.urls import reverse

from ..posts.models import Post
from ..topics.models import Topic
from ..topics.private.models import TopicPrivate

private_topics = TopicPrivate.objects.all()


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
    is_admin = models.BooleanField('Administrator status', default=False)
    is_mod = models.BooleanField('moderator status', default=False)
    birthday = models.DateField('Birthday', null=True)

    def get_absolute_url(self):
        return reverse('frilium:users:profile', args=[self.username])

    @property
    def post_count(self):
        return Post.objects.select_related().filter(user=self).exclude(topic__private_topics__in=private_topics).count()

    @property
    def topic_count(self):
        return Topic.objects.select_related().filter(user=self).exclude(private_topics__in=private_topics).count()

    @property
    def last_post(self):
        posts = Post.objects.filter(user=self).exclude(topic__private_topics__in=private_topics).order_by('-created_at')
        if posts:
            return posts[0].created_at
        else:
            return None

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_admin = True

        if self.is_admin:
            self.is_mod = True
        super().save(*args, **kwargs)
