from django.contrib.auth.models import AbstractUser
from django.urls import reverse

from boards.models import Post


class User(AbstractUser):

    def get_absolute_url(self):
        return reverse('users:user_profile', kwargs={'username': self.username})

    def all_posts(self):
        return Post.objects.filter(created_by=self).order_by('-created_at').all()
