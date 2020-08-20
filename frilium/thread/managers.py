from django.db import models


class TopicQuerySet(models.QuerySet):
    def public(self):
        return self.filter(board__is_private=False)
