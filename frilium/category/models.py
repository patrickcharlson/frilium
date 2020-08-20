from autoslug import AutoSlugField
from django.db import models
from django.utils.html import escape
from django.utils.safestring import mark_safe

from frilium.post.models import Post
from frilium.thread.models import Topic


class Category(models.Model):
    name = models.CharField(max_length=254)
    slug = AutoSlugField(unique=True, always_update=True, populate_from='name')
    color = models.CharField('color', max_length=7, default='#007bff')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    @property
    def topic_count(self):
        return Topic.objects.select_related().filter(board__category=self).count()

    @property
    def post_count(self):
        return Post.objects.select_related().filter(topic__board__category=self).count()

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = f'<span class="badge badge-primary" style="background-color: {color}!important">{name}</span>'
        return mark_safe(html)
