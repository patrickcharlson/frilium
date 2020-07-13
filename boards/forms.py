from django import forms
from django.forms import ModelForm

from .models import Topic, Post


class TopicForm(ModelForm):
    title = forms.CharField(label='', max_length=254, widget=forms.TextInput(attrs={'placeholder': 'Topic title'}))
    message = forms.CharField(label='', widget=forms.Textarea())

    class Meta:
        model = Topic
        fields = ['title', 'message']


class NewTopicForm(TopicForm):
    pass


class PostForm(ModelForm):
    message = forms.CharField(label='', widget=forms.Textarea())

    class Meta:
        model = Post
        fields = ['message', ]


class EditTopicForm(ModelForm):
    title = forms.CharField(label='', max_length=255)

    class Meta:
        model = Topic
        fields = ['title', ]


class EditPostForm(PostForm):
    pass
