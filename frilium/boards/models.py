from autoslug import AutoSlugField
from django.conf import settings
from django.db import models
from django.urls import reverse

from frilium.category.models import Category
from frilium.post.models import Post


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    category = models.ForeignKey(Category, related_name='boards', on_delete=models.CASCADE)
    slug = AutoSlugField(unique=True, always_update=False, populate_from='name')
    description = models.CharField(max_length=100, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_private = models.BooleanField('private', default=False)

    class Meta:
        verbose_name = 'Board'
        verbose_name_plural = 'Boards'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        if self.pk == settings.TOPIC_PRIVATE_BOARD_PK:
            return reverse('frilium:boards:private:index')
        else:
            return reverse('frilium:boards:private:private-posts', args=[self.slug, self.pk])

    @property
    def post_count(self):
        return Post.objects.select_related().filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.select_related().filter(topic__board=self).order_by('-created_at').first()

    @property
    def topic_count(self):
        return self.topics.count()
