from django.db import models


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name
