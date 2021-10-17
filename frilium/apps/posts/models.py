from autoslug import AutoSlugField
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import Truncator
from markdown import markdown

from .managers import PostQuerySet
from ..topics.models import Topic


class Post(models.Model):
    message = models.TextField()
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    slug = AutoSlugField(unique=True, always_update=True, populate_from='message')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='+', on_delete=models.CASCADE)
    last_likes = JSONField(blank=True, null=True)
    likes = models.PositiveIntegerField(default=0)

    objects = PostQuerySet.as_manager()

    class Meta:
        get_latest_by = 'created_at'
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)

    def get_absolute_url(self):
        return reverse('frilium:boards:posts', args=[self.slug])

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))

    def url(self):
        """Returns url for a specific posts"""
        return reverse('frilium:posts:posts', args=[self.slug])
