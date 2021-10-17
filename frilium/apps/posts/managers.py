from django.db import models

from frilium.apps.topics.private.models import TopicPrivate

private_topics = TopicPrivate.objects.all()


class PostQuerySet(models.QuerySet):
    def private(self):
        return self.exclude(topic__private_topics__in=private_topics)
