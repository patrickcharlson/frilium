from django.db import models


def permissions_default():
    return {}


class Role(models.Model):
    name = models.CharField(max_length=100)
    special_role = models.CharField(max_length=100, null=True, blank=True)
    permissions = models.JSONField(default=permissions_default)

    def __str__(self):
        return self.name
