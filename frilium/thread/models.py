from autoslug import AutoSlugField
from django.conf import settings
from django.db import models
from django.urls import reverse

from frilium.thread.managers import TopicQuerySet


class Topic(models.Model):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(unique=True, always_update=True, populate_from='title')
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    board = models.ForeignKey('frilium_boards.Board', related_name='topics', verbose_name='Board',
                              on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='topics', verbose_name='User',
                                   on_delete=models.CASCADE)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='+', on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    is_pinned = models.BooleanField('Pinned', default=False)
    is_globally_pinned = models.BooleanField('Globally pinned', default=False)
    is_closed = models.BooleanField('closed', default=False)
    is_removed = models.BooleanField('removed', default=False)

    objects = TopicQuerySet.as_manager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.pk == 1:
            return reverse('frilium:thread:private:index')
        else:
            return reverse('frilium:thread:topic', args=[self.slug, self.pk])

    def last_post(self):
        return self.posts.select_related().latest()

    def url(self):
        return reverse('frilium:thread:topic', args=[self.slug, self.pk])

    @property
    def first_post(self):
        return self.posts.select_related().order_by('created_at').first()

    # @property
    # def first_post_id(self):
    #     post_id = Post.objects.select_related().filter(thread=self).order_by('created_at')
    #     if post_id:
    #         return post_id[0].id
    #     else:
    #         return None
