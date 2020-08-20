from django.conf import settings
from django.db import models
from django.utils import timezone

from frilium.thread.models import Topic


class TopicPrivate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='private_topics', on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, related_name='private_topics', on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'private thread'
        verbose_name_plural = 'private topics'
        ordering = ['-date', '-pk']
