from django import forms
from django.forms import ModelForm

from .models import Topic, Post


class NewTopicForm(ModelForm):
    message = forms.CharField(label='', widget=forms.Textarea())

    class Meta:
        model = Topic
        fields = ['title', 'message']


class PostForm(ModelForm):
    message = forms.CharField(label='', widget=forms.Textarea())

    class Meta:
        model = Post
        fields = ['message', ]


class EditTopicForm(ModelForm):
    title = forms.CharField(label='Title', max_length=255)

    class Meta:
        model = Topic
        fields = ['title', ]


class EditPostForm(PostForm):
    pass
