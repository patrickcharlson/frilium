from django import forms

from frilium.apps.topics.models import Topic


class TopicForm(forms.ModelForm):
    title = forms.CharField(label='', max_length=254, widget=forms.TextInput(attrs={'placeholder': 'Topic title'}))
    message = forms.CharField(label='', widget=forms.Textarea())

    class Meta:
        model = Topic
        fields = ['title', 'message']


class NewTopicForm(TopicForm):
    pass


class EditTopicForm(forms.ModelForm):
    title = forms.CharField(label='', max_length=255)

    class Meta:
        model = Topic
        fields = ['title', ]
