from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import escape
from django.utils.safestring import mark_safe

from .managers import CategoryQuerySet
from ..core.conf import settings
from ..posts.models import Post
from ..topics.models import Topic
from ..topics.private.models import TopicPrivate

private_topics = TopicPrivate.objects.all()


class Category(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=254)
    slug = AutoSlugField(unique=True, always_update=True, populate_from='title')
    description = models.CharField(max_length=100, blank=True)
    modified = models.DateTimeField(default=timezone.now)
    color = models.CharField('color', max_length=7, default='#007bff')
    is_removed = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)

    objects = CategoryQuerySet.as_manager()

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.pk == settings.TOPIC_PRIVATE_CATEGORY_PK:
            return reverse('frilium:topics:private:index')

        return reverse('frilium:categories:view', kwargs={'pk': str(self.pk), 'slug': self.slug})

    def get_last_post(self):
        return Post.objects.select_related().filter(topic__category=self).exclude(
            topic__private_topics__in=private_topics).order_by(
            '-created_at').first()

    def is_subcategory(self):
        if self.parent_id:
            return True
        return False

    @property
    def url(self):
        return reverse('frilium:categories:view', args=[self.slug, self.pk])

    @property
    def topic_count(self):
        return Topic.objects.select_related().filter(category=self).private().count()

    @property
    def post_count(self):
        return (
            Post.objects
                .select_related()
                .filter(topic__category=self)
                .private()
                .count())

    def get_html_badge(self):
        title = escape(self.title)
        color = escape(self.color)
        html = f'<span class="badge badge-primary" style="background-color: {color}!important">{title}</span>'
        return mark_safe(html)
