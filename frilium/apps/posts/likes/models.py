from django.db import models
from django.utils import timezone

from ...core.conf import settings
from ...core.models import object_relation_base_factory

LikeableObject = object_relation_base_factory(is_required=True)


class PostLike(LikeableObject, models.Model):
    liked_on = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        app_label = 'likes'
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        ordering = ['-pk']

    def __str__(self):
        return f'{self.user} likes {self.content_object}'
