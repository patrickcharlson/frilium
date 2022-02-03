from django.db import models, transaction

from ...core.utils.views import slugify


class RankManager(models.Manager):
    def get_default(self):
        return self.get(is_default=True)

    def mark_as_default(self, rank):
        with transaction.atomic():
            self.filter(is_default=True).update(is_default=False)
            rank.is_default = True
            rank.save(update_fields=['is_default'])


class Rank(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(unique=True, max_length=100)
    description = models.TextField(null=True, blank=True)
    roles = models.ManyToManyField('ace.Role', blank=True)
    is_default = models.BooleanField(default=False)

    objects = RankManager()

    def __str__(self):
        return self.name

    def set_name(self, name):
        self.name = name
        self.slug = slugify(name)
