from django import forms

from .models import Topic, Post


class NewTopicForm(forms.ModelForm):
    message = forms.CharField(label='', widget=forms.Textarea())

    class Meta:
        model = Topic
        fields = ['title', 'message']


class PostForm(forms.ModelForm):
    message = forms.CharField(label='', widget=forms.Textarea())

    class Meta:
        model = Post
        fields = ['message', ]
