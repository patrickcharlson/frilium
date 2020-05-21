from autoslug import AutoSlugField
from django.conf import settings
from django.db import models
from django.urls import reverse


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = AutoSlugField(unique=True, always_update=False, populate_from='name')
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('board_topics', kwargs={'slug': self.slug})


class Topic(models.Model):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(unique=True, always_update=False, populate_from='title')
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    board = models.ForeignKey(Board, related_name='topics', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    slug = AutoSlugField(unique=True, always_update=False, populate_from='topic')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='+', on_delete=models.CASCADE)
