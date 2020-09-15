from .forms import PrivateTopicInviteForm
from ...core.tags.registry import register


@register.inclusion_tag('frilium/thread/private/_invite_form.html')
def render_invite_form(topic, next_=None):
    form = PrivateTopicInviteForm()
    return {'form': form, 'topic': topic, 'next': next_}
