from django.db import models
from django.db.models import Q


class TopicQuerySet(models.QuerySet):
    def unremoved(self):
        return self.filter(
            Q(category__parent=None) | Q(category__parent__is_removed=False),
            category__is_removed=False,
            is_removed=False)

    def public(self):
        return self.filter(category__is_private=False)

    def visible(self):
        return self.unremoved().public()

    def for_category(self, category):
        if category.is_subcategory:
            return self.filter(category=category)

        return self.filter(Q(category=category) | Q(category_parent=category))
