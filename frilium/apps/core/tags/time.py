from datetime import datetime

from django.template import defaultfilters
from django.utils.timezone import is_aware, utc
from django.utils.translation import gettext_lazy, ngettext_lazy

from .registry import register


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
        'year': ngettext_lazy('%d year', '%d years'),
        'month': ngettext_lazy('%d month', '%d months'),
        'week': ngettext_lazy('%d week', '%d weeks'),
        'day': ngettext_lazy('%d day', '%d days'),
        'hour': ngettext_lazy('%d hour', '%d hours'),
        'minute': ngettext_lazy('%d minute', '%d minutes'),
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
