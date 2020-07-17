import hashlib

from django import template
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.safestring import mark_safe

register = template.Library()

User = get_user_model()


@register.filter
def profile_link(user):
    data = f'<a href="{reverse("users:user_posts", args=[user.username, user.pk])}">{user.username}</a>'
    return mark_safe(data)


@register.filter
def gravatar(user):
    email = user.email.lower().encode('utf-8')
    default = 'mm'
    size = 256
    url = f'https://www.gravatar.com/avatar/{hashlib.md5(email).hexdigest()}?{urlencode({"d": default, "s": str(size)})}'
    return url
