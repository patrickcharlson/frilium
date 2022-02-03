from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.db.models import TextChoices
from django.urls import reverse
from django.utils import timezone

from ..posts.models import Post
from ..topics.models import Topic
from ..topics.private.models import TopicPrivate

private_topics = TopicPrivate.objects.all()


class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):

        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Gender(TextChoices):
        NOT_SPECIFIED = '', 'Not Specified'
        MALE = 'Male', 'Male'
        FEMALE = 'Female', 'Female'

    username = models.CharField('Username', max_length=30, unique=True)
    email = models.EmailField(max_length=255, db_index=True, unique=True)
    bio = models.TextField('Bio', max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField('Date joined', default=timezone.now)
    location = models.CharField('Location', max_length=30, blank=True)
    gender = models.CharField('Gender', max_length=50, choices=Gender.choices, default=Gender.NOT_SPECIFIED)
    website = models.URLField('Website', max_length=30, blank=True)
    timezone = models.CharField('Time zone', max_length=32, default='UTC')
    name = models.CharField("Real name", blank=True, max_length=255)
    twitter = models.CharField('Twitter handle', max_length=20, blank=True)
    is_admin = models.BooleanField('Administrator status', default=False)
    is_mod = models.BooleanField('moderator status', default=False)
    birthday = models.DateField('Birthday', null=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('frilium:users:profile', args=[self.username])

    @property
    def post_count(self):
        return Post.objects.select_related().filter(user=self).exclude(topic__private_topics__in=private_topics).count()

    @property
    def topic_count(self):
        return Topic.objects.select_related().filter(user=self).exclude(private_topics__in=private_topics).count()

    @property
    def last_post(self):
        posts = Post.objects.filter(user=self).exclude(topic__private_topics__in=private_topics).order_by('-created_at')
        if posts:
            return posts[0].created_at
        else:
            return None

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_admin = True

        if self.is_admin:
            self.is_mod = True
        super().save(*args, **kwargs)
