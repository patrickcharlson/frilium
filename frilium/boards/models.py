from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe

from ..category.models import Category
from ..core.conf import settings
from ..post.models import Post
from ..thread.private.models import TopicPrivate

private_topics = TopicPrivate.objects.all()


class Board(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, unique=True)
    category = models.ForeignKey(Category, related_name='boards', on_delete=models.CASCADE)
    slug = AutoSlugField(unique=True, always_update=False, populate_from='name')
    description = models.CharField(max_length=100, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    color = models.CharField('color', max_length=7, default='#172b4d')
    is_private = models.BooleanField('private', default=False)
    is_removed = models.BooleanField('removed', default=False)
    is_global = models.BooleanField('global', default=True)

    class Meta:
        verbose_name = 'Board'
        verbose_name_plural = 'Boards'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        if self.pk == settings.TOPIC_PRIVATE_BOARD_PK:
            return reverse('frilium:boards:private:index')
        else:
            return reverse('frilium:thread:board_topics', args=[self.slug])

    @property
    def post_count(self):
        return Post.objects.select_related().filter(topic__board=self).exclude(
            topic__private_topics__in=private_topics).count()

    def get_last_post(self):
        return Post.objects.select_related().filter(topic__board=self).exclude(
            topic__private_topics__in=private_topics).order_by(
            '-created_at').first()

    @property
    def topic_count(self):
        return self.topics.exclude(private_topics__in=private_topics).count()

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = f'<span class="badge badge-primary" style="background-color: {color}!important">{name}</span>'
        return mark_safe(html)
