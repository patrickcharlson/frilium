from django.conf import settings
from django.db import models
from django.utils import timezone

from .managers import PrivateTopicQuerySet


class TopicPrivate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='private_topics', on_delete=models.CASCADE)
    topic = models.ForeignKey('frilium_thread.Topic', related_name='private_topics', on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    is_owner = models.BooleanField(default=False)

    objects = PrivateTopicQuerySet.as_manager()

    class Meta:
        verbose_name = 'private thread'
        verbose_name_plural = 'private topics'

    def get_absolute_url(self):
        return self.topic.get_absolute_url()
