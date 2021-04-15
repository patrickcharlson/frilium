from django.conf import settings
from django.db import models
from django.db.models import TextChoices
from django.utils import timezone


class Report(models.Model):
    class Reason(TextChoices):
        SELECT_REASON = '', 'Select a reason'
        ABUSE = 'Abuse', 'Abuse'
        SPAM = 'Spam', 'Spam'
        OFF_TOPIC = 'Off Topic', 'Off Topic'

    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reports', on_delete=models.CASCADE)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
    body = models.TextField('What would you like to report?', blank=True)
    reason = models.CharField('reason', max_length=50, choices=Reason.choices, default=Reason.SELECT_REASON)

    class Meta:
        verbose_name = 'report'
        verbose_name_plural = 'reports'
        ordering = ['-created_on', '-pk']

    def __str__(self):
        return self.reported_by
