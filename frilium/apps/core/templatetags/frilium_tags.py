import hashlib
from datetime import datetime
from urllib.parse import quote

from django import template
from django.contrib.contenttypes.models import ContentType
from django.template import defaultfilters
from django.template.loader import render_to_string
from django.utils.http import urlencode
from django.utils.timezone import is_aware, utc
from django.utils.translation import ngettext_lazy, gettext_lazy, npgettext_lazy

from ...posts.likes.models import PostLike
from ...topics.private.forms import PrivateTopicInviteForm

register = template.Library()


@register.simple_tag()
def avatar_url(user, size, rating='g', default='identicon'):
    url = "https://www.gravatar.com/avatar/"
    hash_ = hashlib.md5(user.email.strip().lower().encode('utf-8')).hexdigest()
    data = urlencode([('d', quote(default)),
                      ('s', str(size)),
                      ('r', rating)])
    return "".join((url, hash_, '?', data))


@register.simple_tag()
def get_avatar_color(user_id):
    hue = (user_id % 37) * 10
    return f'hsl({hue}, 75%, 25%)'


@register.filter
def humanizetime(value):
    return HumanizeNaturalTime.time_string(value)


class HumanizeNaturalTime:
    time_strings = {
        'past-day': gettext_lazy('%(delta)s ago'),
        'past-hour': ngettext_lazy('an hour ago', '%(count)s hours ago', 'count'),
        'past-minute': ngettext_lazy('a minute ago', '%(count)s minutes ago', 'count'),
        'past-second': ngettext_lazy('a second ago', '%(count)s seconds ago', 'count'),
        'now': gettext_lazy('now'),
    }
    past_substrings = {
        'year': npgettext_lazy('naturaltime-past', '%(num)d year', '%(num)d years', 'num'),
        'month': npgettext_lazy('naturaltime-past', '%(num)d month', '%(num)d months', 'num'),
        'week': npgettext_lazy('naturaltime-past', '%(num)d week', '%(num)d weeks', 'num'),
        'day': npgettext_lazy('naturaltime-past', '%(num)d day', '%(num)d days', 'num'),
        'hour': npgettext_lazy('naturaltime-past', '%(num)d hour', '%(num)d hours', 'num'),
        'minute': npgettext_lazy('naturaltime-past', '%(num)d minute', '%(num)d minutes', 'num'),
    }

    @classmethod
    def time_string(cls, value):

        now = datetime.now(utc if is_aware(value) else None)
        if value < now:
            delta = now - value
            if delta.days:
                return cls.time_strings['past-day'] % {
                    'delta': defaultfilters.timesince(value, now, time_strings=cls.past_substrings).split(', ')[0],
                }
            elif delta.seconds == 0:
                return cls.time_strings['now']
            elif delta.seconds < 60:
                return cls.time_strings['past-second'] % {'count': delta.seconds}
            elif delta.seconds // 60 < 60:
                count = delta.seconds // 60
                return cls.time_strings['past-minute'] % {'count': count}
            else:
                count = delta.seconds // 60 // 60
                return cls.time_strings['past-hour'] % {'count': count}


@register.inclusion_tag('frilium/topics/private/_invite_form.html')
def render_invite_form(topic, next_=None):
    form = PrivateTopicInviteForm()
    return {'form': form, 'topic': topic, 'next': next_}


class ObjectLikeWidget(template.Node):
    def __init__(self, var):
        self.var = var

    def render(self, context):
        liked_object = self.var.resolve(context)
        ct = ContentType.objects.get_for_model(liked_object)
        user = context["request"].user

        if not user.is_authenticated:
            return ""

        context.push(object=liked_object, content_type_id=ct.pk)
        output = render_to_string("likes/includes/widget.html", context.flatten())
        context.pop()
        return output


@register.tag
def like_widget(parser, token):
    try:
        tag_name, for_str, var_name = token.split_contents()
    except ValueError:
        tag_name = "%r" % token.contents.split()[0]
        raise template.TemplateSyntaxError(
            f"{tag_name} tag requires a following syntax: "
            f"{{% {tag_name} for <object> %}}"
        )
    var = template.Variable(var_name)
    return ObjectLikeWidget(var)


@register.filter
def liked_by(obj, user):
    ct = ContentType.objects.get_for_model(obj)
    liked = PostLike.objects.filter(user=user, content_type=ct, object_id=obj.pk)
    return liked.count() > 0


@register.filter
def liked_count(obj):
    ct = ContentType.objects.get_for_model(obj)
    likes = PostLike.objects.filter(content_type=ct, object_id=obj.pk)
    return likes.count()
