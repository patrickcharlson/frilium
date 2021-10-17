from django import forms
from django.contrib.auth import get_user_model

from .models import TopicPrivate
from ..models import Topic
from ...categories.models import Category
from ...core.conf import settings
from ...core.utils.widgets import MultipleInput

User = get_user_model()


class TopicPrivateForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', ]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['title'].label = ''
        self.fields['title'].widget.attrs.update({'placeholder': 'Topic title'})
        self._category = None

    @property
    def category(self):
        if self._category:
            return self._category
        self._category = Category.objects.get(pk=settings.TOPIC_PRIVATE_CATEGORY_PK)
        return self._category

    def save(self, commit=True):
        if not self.instance.pk:
            self.instance.user = self.user
            self.instance.category = self.category
        return super().save(commit)


def multiple_input(*args, **kwargs):
    return MultipleInput(*args, **kwargs)


class TopicPrivateManyForm(forms.Form):
    users = forms.ModelMultipleChoiceField(queryset=User.objects.all(),
                                           to_field_name=User.USERNAME_FIELD)

    def __init__(self, *args, user=None, topic=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['users'].widget = multiple_input(attrs={'placeholder': 'Patrick, Peppa, Liam,...'})
        self.fields['users'].label = ''
        self.user = user
        self.topic = topic

    def clean_users(self):
        users = set(self.cleaned_data['users'])
        if self.user not in users:
            users.add(self.user)
        return users

    def get_users(self):
        users = set(self.cleaned_data['users'])
        users.remove(self.user)
        return users

    def save_m2m(self):
        users = self.cleaned_data['users']
        return TopicPrivate.objects.bulk_create(
            [TopicPrivate(user=user, topic=self.topic) for user in users]
        )


def cx_text_input(*args, **kwargs):
    return forms.TextInput(*args, **kwargs)


class PrivateTopicInviteForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(),
                                  to_field_name=User.USERNAME_FIELD,
                                  label='')

    def __init__(self, *args, topic=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.topic = topic
        self.fields['user'].widget = cx_text_input(attrs={'placeholder': ''})

    class Meta:
        model = TopicPrivate
        fields = ['user']

    def clean_user(self):
        user = self.cleaned_data['user']
        private = TopicPrivate.objects.filter(user=user, topic=self.topic)

        if private.exists():
            raise forms.ValidationError(
                "%(username)s is already a participant" % {'username': user.username})
        return user

    def get_user(self):
        return self.cleaned_data['user']

    def save(self, commit=True):
        if not self.instance.pk:
            self.instance.topic = self.topic
        return super().save(commit)
