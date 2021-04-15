from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse

from .managers import TopicQuerySet
from .private.models import TopicPrivate
from ..core.conf import settings


class Topic(models.Model):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(unique=True, always_update=True, populate_from='title')
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('categories.Category', related_name='topics', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='topics', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='+', on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    is_removed = models.BooleanField(default=False)

    objects = TopicQuerySet.as_manager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.category_id == settings.TOPIC_PRIVATE_CATEGORY_PK:
            return reverse('frilium:topics:private:view', args=[self.slug, self.pk])
        else:
            return reverse('frilium:topics:view', args=[self.slug, self.pk])

    def last_post(self):
        return self.posts.select_related().latest()

    def url(self):
        return reverse('frilium:topics:topic', args=[self.slug, self.pk])

    @property
    def first_post(self):
        return self.posts.select_related().order_by('created_at').first()
