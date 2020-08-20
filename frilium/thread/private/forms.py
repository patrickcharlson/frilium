from django import forms
from django.contrib.auth import get_user_model
from django.utils.encoding import smart_bytes

from .models import TopicPrivate

from frilium.core import utils
from frilium.core.conf.settings import settings
from frilium.core.utils.widgets import MultipleInput
from ..models import Topic
from ...boards.models import Board

User = get_user_model()


class TopicPrivateForm(forms.ModelForm):
    topic_hash = forms.CharField(max_length=32, widget=forms.HiddenInput, required=False)

    class Meta:
        model = Topic
        fields = ['title', ]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['title'].label = ''
        self.fields['title'].widget.attrs.update({'placeholder': 'Topic title'})
        self._board = None

    @property
    def board(self):
        if self._board:
            return self._board
        self._board = Board.objects.get(pk=settings.TOPIC_PRIVATE_BOARD_PK)
        return self._board

    def get_topic_hash(self):
        topic_hash = self.cleaned_data.get('topic_hash', None)
        if topic_hash:
            return topic_hash

        return utils.get_hash((
            smart_bytes(self.cleaned_data['title']),
            smart_bytes('board-{}'.format(self.board.pk))
        ))

    def save(self, commit=True):
        if not self.instance.pk:
            self.instance.user = self.user
            self.instance.board = self.board
        return super().save(commit)


def multiple_input(*args, **kwargs):
    return MultipleInput(*args, **kwargs)


class TopicPrivateManyForm(forms.Form):
    users = forms.ModelMultipleChoiceField(queryset=User.objects.all(),
                                           to_field_name=User.USERNAME_FIELD)

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['users'].widget = multiple_input(attrs={'placeholder': 'Patrick, Peppa, Liam,...'})
        self.fields['users'].label = ''
        self.user = user

    def save_m2m(self):
        users = self.cleaned_data['users']
        return TopicPrivate.objects.bulk_create(
            [TopicPrivate(user=user, topic=self.topic) for user in users]
        )
